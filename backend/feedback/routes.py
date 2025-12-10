from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse, PlainTextResponse
from typing import AsyncIterator
import asyncio, json
from .repository import get_report
from .eventbus import subscribe
from .models import SessionBundleRef
from .metrics import metrics_response

router = APIRouter()

@router.get("/v1/health")
async def health():
    return {"status": "ok"}

@router.get("/v1/metrics")
async def metrics():
    ctype, payload = metrics_response()
    return PlainTextResponse(payload, media_type=ctype)

@router.post("/v1/feedback/analyze")
async def analyze_now(bundle: SessionBundleRef):
    # Direct on-demand analyze; in production enqueue to Redis for worker processing.
    return {"accepted": True, "session_id": bundle.session_id}

@router.get("/v1/feedback/{session_id}")
async def get_feedback(session_id: str):
    data = await get_report(session_id)
    if not data:
        raise HTTPException(404, "Report not found")
    return data

@router.get("/v1/feedback/stream")
async def stream(session_id: str):
    q = subscribe(session_id)
    async def gen() -> AsyncIterator[bytes]:
        while True:
            msg = await q.get()
            yield f"event: {msg.get('event','message')}\n".encode()
            yield f"data: {json.dumps(msg)}\n\n".encode()
    return StreamingResponse(gen(), media_type="text/event-stream")
