import httpx
from fastapi import APIRouter, Request, Response
from ..config import settings
router = APIRouter()

@router.post("/v1/tts")
async def tts(request: Request, payload: dict):
    cid = request.headers.get("x-correlation-id","")
    sid = request.headers.get("x-session-id","")
    headers = {"x-correlation-id": cid, "x-session-id": sid}
    async with httpx.AsyncClient(timeout=None) as client:
        async with client.stream("POST", f"{settings.TTS_URL}/v1/tts", json=payload, headers=headers) as resp:
            resp.raise_for_status()
            async def aiter():
                async for chunk in resp.aiter_bytes():
                    yield chunk
            return Response(aiter(), media_type=resp.headers.get("content-type","application/octet-stream"))
