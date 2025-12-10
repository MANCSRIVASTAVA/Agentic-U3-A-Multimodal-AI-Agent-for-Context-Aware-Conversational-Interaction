# Services/LLM/app/stream.py
from __future__ import annotations
import asyncio
from typing import AsyncGenerator, Optional
from app.sse import sse_event

async def chunked_sse(text: str, provider: str, model: Optional[str] = None) -> AsyncGenerator[bytes, None]:
    for token in text.split():
        yield sse_event("llm.token", {"delta": token + " ", "provider": provider}).encode("utf-8")
        await asyncio.sleep(0)
    yield sse_event("llm.done", {
        "model": model or "",
        "provider": provider,
        "usage": {},
        "fallback_used": provider != "openai",
    }).encode("utf-8")
