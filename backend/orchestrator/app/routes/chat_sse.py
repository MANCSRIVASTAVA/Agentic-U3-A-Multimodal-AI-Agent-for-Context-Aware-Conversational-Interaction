import json
from fastapi import APIRouter, Request
from ..sse import sse_response, format_event
from ..agent.router import run_turn

router = APIRouter()

@router.get("/v1/chat/sse")
async def chat_sse(request: Request, text: str, voice: bool = False):
    cid = request.headers.get("x-correlation-id","")
    sid = request.headers.get("x-session-id","")
    async def gen():
        async for event in run_turn(text, voice, cid, sid):
            if event["event"].startswith("tts.audio."):
                yield format_event("tool.status", json.dumps({"note":"audio omitted over SSE"}))
            else:
                yield format_event(event["event"], json.dumps(event["data"]))
    return sse_response(gen())
