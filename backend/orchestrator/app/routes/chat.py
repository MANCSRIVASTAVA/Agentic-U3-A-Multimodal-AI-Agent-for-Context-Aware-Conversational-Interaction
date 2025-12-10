from __future__ import annotations

import asyncio
import json
import time
from typing import AsyncGenerator, Dict, List, Optional

import httpx
from fastapi import APIRouter, Depends, Header, HTTPException, Request, Response, status
from fastapi.responses import JSONResponse, StreamingResponse

# If you have helpers in shared/, import them; fallback to local minimal shims if not.
try:
    from shared.logging import get_logger
    from shared.metrics import (
        Counter,
        Histogram,
        registry as _metrics_registry,  # noqa
    )
    from shared.sse import sse_event  # returns bytes for a single SSE frame
except Exception:  # minimal shims if shared/ isn't vendored yet
    import logging
    logger = logging.getLogger("chat")
    logging.basicConfig(level=logging.INFO)

    def get_logger(name="chat"):
        return logging.getLogger(name)

    class Counter:
        def __init__(self, *_a, **_k): pass
        def labels(self, **_k): return self
        def inc(self, *_a, **_k): pass

    class Histogram:
        def __init__(self, *_a, **_k): pass
        def labels(self, **_k): return self
        def observe(self, *_a, **_k): pass

    def sse_event(event: str, data: dict) -> bytes:
        return (f"event: {event}\n" + "data: " + json.dumps(data, ensure_ascii=False) + "\n\n").encode("utf-8")

from ..config import settings

router = APIRouter(prefix="/v1", tags=["chat"])
log = get_logger("orchestrator.chat")

# ---------- Metrics ----------
CHAT_REQ_TOTAL = Counter(
    "chat_requests_total", "Number of chat requests",
    labelnames=["mode", "used_rag"]
)
CHAT_FIRST_TOKEN_MS = Histogram(
    "chat_first_token_ms", "First token latency in milliseconds",
    labelnames=["provider"]
)
CHAT_TOKENS_STREAMED = Counter(
    "chat_tokens_streamed_total", "Tokens streamed to client",
    labelnames=["provider"]
)
CHAT_FALLBACK = Counter(
    "chat_fallback_total", "Fallbacks observed (as-reported by LLM)",
    labelnames=["provider"]
)

# ---------- Helpers ----------
def _should_use_rag(query: str, use_rag_flag: Optional[bool]) -> bool:
    if use_rag_flag is True:
        return True
    if use_rag_flag is False:
        return False
    # heuristic: use RAG for longer questions (customize as you like)
    return len(query.strip()) >= settings.RAG_AUTO_LENGTH_THRESHOLD

async def _retrieve_context(query: str, authorization: Optional[str]) -> List[Dict]:
    """Call RAG /v1/retrieve top_k=3 and return results list."""
    rag_url = settings.RAG_URL.rstrip("/") + "/v1/retrieve"
    params = {"q": query, "top_k": 3}
    headers = {}
    if authorization:
        headers["Authorization"] = authorization

    timeout = httpx.Timeout(15.0, connect=5.0)
    async with httpx.AsyncClient(timeout=timeout) as client:
        r = await client.get(rag_url, params=params, headers=headers)
        if r.status_code != 200:
            log.warning("RAG retrieve failed: %s %s", r.status_code, r.text)
            return []
        payload = r.json()
        return payload.get("results", [])

async def _emit_analytics(event_name: str, data: Dict, authorization: Optional[str]) -> None:
    """Fire-and-forget analytics emit; never block the response path."""
    if not settings.ANALYTICS_URL:
        return
    url = settings.ANALYTICS_URL.rstrip("/") + "/v1/ingest"
    headers = {"Content-Type": "application/json"}
    if authorization:
        headers["Authorization"] = authorization

    async def _do():
        try:
            async with httpx.AsyncClient(timeout=httpx.Timeout(5.0, connect=2.0)) as client:
                await client.post(url, json={"event": event_name, "data": data}, headers=headers)
        except Exception as e:
            log.debug("Analytics emit failed: %s", e)

    asyncio.create_task(_do())

async def _stream_llm_sse(
    prompt: str,
    context_snippets: Optional[List[Dict]],
    authorization: Optional[str],
) -> AsyncGenerator[bytes, None]:
    """
    Connect to LLM /v1/generate (SSE), pipe events to client, track first token latency,
    count tokens, and forward final done event with provenance if used.
    """
    llm_url = settings.LLM_URL.rstrip("/") + "/v1/generate"
    headers = {"Accept": "text/event-stream"}
    if authorization:
        headers["Authorization"] = authorization

    body = {
        "prompt": prompt,  # keep for providers that accept plain prompt
        "messages": [
            {"role": "user", "content": prompt}
        ],                 # add for chat-style providers
        "stream": True,
    }
    if context_snippets:
        body["context"] = context_snippets  # the LLM service can optionally leverage this

    provider_seen: Optional[str] = None
    first_token_ms: Optional[float] = None
    t0 = time.perf_counter()

    timeout = httpx.Timeout(30.0, connect=5.0)
    async with httpx.AsyncClient(timeout=timeout) as client:
        try:
            async with client.stream("POST", llm_url, json=body, headers=headers) as resp:
                if resp.status_code != 200:
                    text = await resp.aread()
                    raise HTTPException(status_code=resp.status_code, detail=text.decode("utf-8", "ignore"))

                buffer = b""
                async for chunk in resp.aiter_bytes():
                    if not chunk:
                        continue
                    buffer += chunk

                    while b"\n\n" in buffer:
                        frame, buffer = buffer.split(b"\n\n", 1)
                        # parse SSE frame
                        event_name = None
                        data_lines: List[bytes] = []
                        for line in frame.split(b"\n"):
                            if line.startswith(b"event:"):
                                event_name = line[len(b"event:"):].strip().decode("utf-8", "ignore")
                            elif line.startswith(b"data:"):
                                data_lines.append(line[len(b"data:"):].strip())

                        if not event_name:
                            # skip comments/keepalives
                            continue

                        data_json: Dict = {}
                        if data_lines:
                            try:
                                data_json = json.loads(b"\n".join(data_lines).decode("utf-8"))
                            except Exception:
                                data_json = {"raw": (b"\n".join(data_lines)).decode("utf-8", "ignore")}

                        # Observe metrics & enrich
                        if event_name == "llm.token":
                            if first_token_ms is None:
                                first_token_ms = (time.perf_counter() - t0) * 1000.0
                                if provider_seen:
                                    CHAT_FIRST_TOKEN_MS.labels(provider=provider_seen).observe(first_token_ms)
                            # count tokens if available
                            CHAT_TOKENS_STREAMED.labels(provider=provider_seen or "unknown").inc()
                        elif event_name == "llm.done":
                            provider_seen = data_json.get("provider") or provider_seen
                            # fallbacks reported by LLM
                            if data_json.get("fallback_used"):
                                CHAT_FALLBACK.labels(provider=provider_seen or "unknown").inc()
                            # attach provenance if we had context snippets
                            if context_snippets is not None:
                                data_json["provenance"] = [
                                    {
                                        "text": s.get("text"),
                                        "score": s.get("score"),
                                        "source_url": s.get("source_url"),
                                        "doc_id": s.get("doc_id"),
                                        "chunk_id": s.get("chunk_id"),
                                    } for s in context_snippets
                                ]
                                # Re-emit the mutated llm.done payload
                                yield sse_event("llm.done", data_json)
                                # Also push analytics (fire-and-forget)
                                await _emit_analytics(
                                    "llm_complete",
                                    {
                                        "provider": data_json.get("provider"),
                                        "model": data_json.get("model"),
                                        "first_token_ms": first_token_ms,
                                        "fallback_used": bool(data_json.get("fallback_used")),
                                    },
                                    authorization
                                )
                                continue

                        # Remember provider if tokens carry it (some impls put it on token frames)
                        if not provider_seen:
                            provider_seen = data_json.get("provider")

                        # pipe original frame through
                        yield sse_event(event_name, data_json)

        except HTTPException:
            raise
        except Exception as e:
            log.exception("LLM streaming error: %s", e)
            err = {"code": "LLM_STREAM_ERROR", "message": "Failed while streaming from LLM", "details": str(e)}
            yield sse_event("error", err)


# ---------- Routes ----------

@router.post("/chat")
async def chat_sync(
    request: Request,
    authorization: Optional[str] = Header(default=None, convert_underscores=False),
):
    """
    Optional sync mode:
    - If use_rag flag (or query length over threshold) -> fetch snippets from RAG
    - Call LLM (still streamed internally), collect into a final string and return JSON
    """
    payload = await request.json()
    query: str = payload.get("query", "") or ""
    use_rag_flag: Optional[bool] = payload.get("use_rag")

    if not query.strip():
        raise HTTPException(status_code=400, detail="query is required")

    will_use_rag = _should_use_rag(query, use_rag_flag)
    CHAT_REQ_TOTAL.labels(mode="sync", used_rag=str(will_use_rag).lower()).inc()

    snippets = await _retrieve_context(query, authorization) if will_use_rag else None

    # Stream internally, concatenate tokens
    final_text_parts: List[str] = []
    first_token_ms: Optional[float] = None
    provider_seen: Optional[str] = None
    t0 = time.perf_counter()

    async for sse_bytes in _stream_llm_sse(query, snippets, authorization):
        # parse our own SSE back
        text = sse_bytes.decode("utf-8", "ignore")
        current_event = None
        for line in text.splitlines():
            if line.startswith("event:"):
                current_event = line.split("event:", 1)[1].strip()
            elif line.startswith("data:"):
                try:
                    data = json.loads(line.split("data:", 1)[1].strip())
                except Exception:
                    data = {}

                if current_event == "llm.token":
                    if first_token_ms is None:
                        first_token_ms = (time.perf_counter() - t0) * 1000.0
                    delta = data.get("delta")
                    if isinstance(delta, str):
                        final_text_parts.append(delta)
                    provider_seen = provider_seen or data.get("provider")
                elif current_event == "llm.done":
                    provider_seen = provider_seen or data.get("provider")

    # Emit analytics once per sync call
    await _emit_analytics(
        "llm_complete",
        {
            "provider": provider_seen,
            "model": None,  # filled by llm.done above in stream path if available; unknown here if not seen
            "first_token_ms": first_token_ms,
            "fallback_used": False,  # unknown unless llm.done observed; conservatively False
        },
        authorization
    )

    return JSONResponse(
        {"text": "".join(final_text_parts), "used_rag": will_use_rag, "provider": provider_seen}
    )


@router.get("/chat/stream")
async def chat_stream(
    q: str,
    use_rag: Optional[bool] = None,
    request: Request = None,  # noqa
    authorization: Optional[str] = Header(default=None, convert_underscores=False),
):
    """
    SSE endpoint:
    - GET /v1/chat/stream?q=...&use_rag=true|false
    - Pipes events from LLM service:
      * llm.token {delta}
      * llm.done  {model,provider,usage,fallback_used}
      * error     {code,message,details}
    - If RAG used, appends provenance to llm.done
    """
    if not q.strip():
        raise HTTPException(status_code=400, detail="q is required")

    will_use_rag = _should_use_rag(q, use_rag)
    CHAT_REQ_TOTAL.labels(mode="sse", used_rag=str(will_use_rag).lower()).inc()

    async def event_gen() -> AsyncGenerator[bytes, None]:
        snippets = await _retrieve_context(q, authorization) if will_use_rag else None
        async for frame in _stream_llm_sse(q, snippets, authorization):
            yield frame

    return StreamingResponse(
        event_gen(),
        status_code=200,
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
        },
    )
