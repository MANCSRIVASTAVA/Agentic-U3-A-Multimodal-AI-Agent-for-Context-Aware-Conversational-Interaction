import asyncio, json, time
from typing import Dict, Any, AsyncIterator
import httpx, backoff
from ..config import settings
from ..metrics import tool_latency

def with_backoff():
    return backoff.on_exception(backoff.expo, (httpx.HTTPError, asyncio.TimeoutError), max_tries=settings.RETRIES+1)

@with_backoff()
async def rag_retrieve(query: str, top_k: int = 3, cid: str = "", sid: str = "") -> Dict[str, Any]:
    url = f"{settings.RAG_URL}/v1/retrieve"
    headers = {"x-correlation-id": cid, "x-session-id": sid}
    t0 = time.time()
    async with httpx.AsyncClient(timeout=settings.REQUEST_TIMEOUT_SECONDS) as client:
        resp = await client.get(url, params={"q": query, "top_k": top_k}, headers=headers)
        resp.raise_for_status()
        data = resp.json()
    tool_latency.labels("rag_retrieve").observe(time.time()-t0)
    return data

@with_backoff()
async def rag_ingest(payload: Dict[str, Any], cid: str = "", sid: str = "") -> Dict[str, Any]:
    url = f"{settings.RAG_URL}/v1/ingest"
    headers = {"x-correlation-id": cid, "x-session-id": sid}
    t0 = time.time()
    async with httpx.AsyncClient(timeout=settings.REQUEST_TIMEOUT_SECONDS) as client:
        resp = await client.post(url, json=payload, headers=headers)
        resp.raise_for_status()
        data = resp.json()
    tool_latency.labels("rag_ingest").observe(time.time()-t0)
    return data

@with_backoff()
async def llm_generate(prompt: str, cid: str = "", sid: str = "") -> str:
    url = f"{settings.LLM_URL}/v1/generate"
    headers = {"x-correlation-id": cid, "x-session-id": sid}
    t0 = time.time()
    async with httpx.AsyncClient(timeout=settings.REQUEST_TIMEOUT_SECONDS) as client:
        resp = await client.post(url, json={"prompt": prompt}, headers=headers)
        resp.raise_for_status()
        data = resp.json()
    tool_latency.labels("llm_generate").observe(time.time()-t0)
    return data.get("text","")

async def tts_speak(text: str, cid: str = "", sid: str = "") -> AsyncIterator[bytes]:
    url = f"{settings.TTS_URL}/v1/tts"
    headers = {"x-correlation-id": cid, "x-session-id": sid}
    t0 = time.time()
    async with httpx.AsyncClient(timeout=None) as client:
        async with client.stream("POST", url, json={"text": text}, headers=headers) as resp:
            resp.raise_for_status()
            async for chunk in resp.aiter_bytes():
                yield chunk
    tool_latency.labels("tts_speak").observe(time.time()-t0)
