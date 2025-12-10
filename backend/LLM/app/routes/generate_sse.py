# Services/LLM/app/routes/generate_sse.py
from __future__ import annotations

import asyncio
import json
import os
import time
from typing import Any, AsyncGenerator, Dict, List, Optional

import httpx
from fastapi import APIRouter, Header, HTTPException, Request
from fastapi.responses import StreamingResponse
from pydantic import BaseModel, Field

# Use your existing SSE helpers
from app.sse import sse_event, heartbeat_comment

router = APIRouter(prefix="/v1", tags=["generate-sse"])

# -------- Request/Response Models (aligned with your existing /v1/generate) --------
class ChatMessage(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    messages: List[ChatMessage] = Field(default_factory=list)
    prompt: Optional[str] = None
    temperature: Optional[float] = 0.2
    stream: Optional[bool] = True
    tools: Optional[List[Dict[str, Any]]] = None
    max_tokens: Optional[int] = 512
    model: Optional[str] = None  # allow override

# -------- Provider Config --------
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "").strip()
OPENAI_BASE_URL = os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1").rstrip("/")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")

HF_API_TOKEN = os.getenv("HF_API_TOKEN", "").strip()
HF_BASE_URL = os.getenv("HF_BASE_URL", "https://api-inference.huggingface.co").rstrip("/")
HF_MODEL = os.getenv("HF_MODEL", "mistralai/Mistral-7B-Instruct-v0.3")

# -------- Helpers --------
def _to_prompt(req: ChatRequest) -> str:
    if req.prompt:
        return req.prompt
    if req.messages:
        # simple concatenation; you already have similar util in orchestrator
        parts = []
        for m in req.messages:
            if m.role == "system":
                parts.append(f"System: {m.content.strip()}")
            elif m.role == "user":
                parts.append(f"User: {m.content.strip()}")
            elif m.role == "assistant":
                parts.append(f"Assistant: {m.content.strip()}")
        parts.append("Assistant:")
        return "\n".join(parts)
    return ""

async def _openai_stream(req: ChatRequest) -> AsyncGenerator[bytes, None]:
    """
    Try native OpenAI streaming. Emits:
      - event: llm.token  data: {"delta": "...", "provider":"openai"}
      - event: llm.done   data: {"model":..., "provider":"openai", "usage": {...}, "fallback_used": false}
    """
    if not OPENAI_API_KEY:
        raise RuntimeError("OPENAI_API_KEY not set")

    url = f"{OPENAI_BASE_URL}/chat/completions"
    headers = {
        "Authorization": f"Bearer {OPENAI_API_KEY}",
        "Content-Type": "application/json",
    }
    # Build chat messages for OpenAI
    messages = req.messages or [{"role": "user", "content": _to_prompt(req)}]
    body = {
        "model": req.model or OPENAI_MODEL,
        "messages": [m if isinstance(m, dict) else m.model_dump() for m in messages],
        "temperature": req.temperature or 0.2,
        "stream": True,
        "max_tokens": req.max_tokens or 512,
    }

    provider = "openai"
    model = body["model"]
    t0 = time.perf_counter()

    timeout = httpx.Timeout(120.0, connect=10.0)
    async with httpx.AsyncClient(timeout=timeout) as client:
        async with client.stream("POST", url, headers=headers, json=body) as resp:
            if resp.status_code != 200:
                text = await resp.aread()
                raise HTTPException(status_code=resp.status_code, detail=text.decode("utf-8", "ignore"))

            # stream Server-Sent Events in OpenAI's data: lines
            async for raw in resp.aiter_lines():
                if not raw:
                    # keepalive for clients
                    yield heartbeat_comment().encode("utf-8")
                    continue
                if raw.startswith("data: "):
                    data = raw[6:]
                else:
                    continue
                if data.strip() == "[DONE]":
                    # done event with minimal usage (OpenAI returns usage only in non-stream)
                    done_payload = {
                        "model": model,
                        "provider": provider,
                        "usage": {},
                        "fallback_used": False,
                    }
                    yield sse_event("llm.done", done_payload).encode("utf-8")
                    break

                try:
                    payload = json.loads(data)
                except Exception:
                    continue

                # Extract delta tokens
                choice = (payload.get("choices") or [{}])[0]
                delta = (choice.get("delta") or {}).get("content")
                if delta:
                    yield sse_event("llm.token", {"delta": delta, "provider": provider}).encode("utf-8")

async def _hf_complete(req: ChatRequest) -> str:
    """
    Non-streaming HF inference as a fallback. Returns the full text.
    """
    if not HF_API_TOKEN:
        raise RuntimeError("HF_API_TOKEN not set")

    url = f"{HF_BASE_URL}"
    headers = {"Authorization": f"Bearer {HF_API_TOKEN}", "Content-Type": "application/json"}
    prompt = _to_prompt(req) or (req.messages[-1].content if req.messages else "")
    body = {
        "messages": req.messages,
        "temperature": req.temperature or 0.2,
        "max_new_tokens": req.max_tokens or 512,
        "return_full_text": False,
        "model": HF_MODEL
    }

    timeout = httpx.Timeout(120.0, connect=10.0)
    async with httpx.AsyncClient(timeout=timeout) as client:
        r = await client.post(url, headers=headers, json=body)
        if r.status_code != 200:
            raise HTTPException(status_code=r.status_code, detail=r.text)
        data = r.json()
        # HF text shapes vary by model; handle common cases
        if isinstance(data, list) and data and "generated_text" in data[0]:
            return data[0]["generated_text"]
        if isinstance(data, dict) and "generated_text" in data:
            return data["generated_text"]
        # Fallback parse
        try:
            return data[0]["generated_text"]
        except Exception:
            # last resort
            return json.dumps(data)[:2000]

async def _emit_chunked_tokens(text: str, provider: str, model: Optional[str]) -> AsyncGenerator[bytes, None]:
    """
    Convert a full text into SSE token events so the orchestrator still
    sees a live stream even when provider can't stream natively.
    """
    # naive chunking by words; you can refine (e.g., by sentencepiece-like sizes)
    for token in text.split():
        yield sse_event("llm.token", {"delta": token + " ", "provider": provider})
        await asyncio.sleep(0)  # allow event loop to flush
    yield sse_event("llm.done", {
        "model": model or "",
        "provider": provider,
        "usage": {},
        "fallback_used": provider != "openai",  # mark true for HF fallback
    })

# -------- The streaming endpoint (SAME PATH as existing JSON /v1/generate) --------
@router.post("/generate")
async def generate_stream(
    request: Request,
    accept: Optional[str] = Header(default=""),
) -> StreamingResponse:
    """
    SSE-aware /v1/generate:
      - If client asks for 'text/event-stream' (or body.stream==True): stream tokens.
      - Prefers OpenAI native streaming when available.
      - Falls back to HF non-streaming + token-chunking (still emits llm.token/llm.done).
      - If neither provider configured, returns 503 via HTTPException.
    This keeps the route compatible with your orchestrator (POST /v1/generate + Accept: text/event-stream).
    """
    try:
        payload = await request.json()
    except Exception:
        payload = {}

    req = ChatRequest(**payload)
    wants_stream = ("text/event-stream" in (accept or "").lower()) or bool(req.stream)

    if not wants_stream:
        # For backwards-compat you may keep your original JSON handler in main.py.
        # Here we force streaming for orchestrator scenario.
        wants_stream = True

    async def gen() -> AsyncGenerator[bytes, None]:
        # Try OpenAI native streaming first
        if OPENAI_API_KEY:
            try:
                async for frame in _openai_stream(req):
                    yield frame
                return
            except Exception as e:
                # Log error but don't emit error event yet - try fallback first
                print(f"OPENAI ERROR: {e}") # logging openai error
                # Don't yield error event here - try fallback first

        # HuggingFace fallback (non-streaming -> chunked SSE)
        if HF_API_TOKEN:
            try:
                text = await _hf_complete(req)
                async for frame in _emit_chunked_tokens(text, provider="huggingface", model=req.model or HF_MODEL):
                    yield frame
                return
            except Exception as e:
                print(f"Hugging Face ERROR: {e}") # logging HF error
                # Only emit error if both providers fail
                yield sse_event("error", {"code": "HF_GENERATE_FAIL", "message": str(e)})
                return

        # If we get here, OpenAI failed and no HF token
        yield sse_event("error", {"code": "OPENAI_STREAM_FAIL", "message": "OpenAI failed and no fallback configured"})

    return StreamingResponse(
        gen(),
        status_code=200,
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
        },
    )
