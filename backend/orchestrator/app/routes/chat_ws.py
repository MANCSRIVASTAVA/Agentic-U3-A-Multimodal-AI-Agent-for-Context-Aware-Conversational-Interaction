import json
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from ..metrics import ws_connections
from ..agent.router import run_turn

router = APIRouter()

@router.websocket("/v1/chat/ws")
async def chat_ws(ws: WebSocket):
    await ws.accept()
    ws_connections.labels("/v1/chat/ws").inc()
    try:
        raw = await ws.receive_text()
        payload = json.loads(raw)
        text = payload.get("text","")
        voice = bool(payload.get("voice", False))
        cid = ws.headers.get("x-correlation-id","")
        sid = payload.get("session_id") or ws.headers.get("x-session-id","")
        async for event in run_turn(text, voice, cid, sid):
            if event["event"].startswith("tts.audio.") and isinstance(event["data"], (bytes, bytearray)):
                await ws.send_bytes(event["data"])
            else:
                await ws.send_text(json.dumps(event))
    except WebSocketDisconnect:
        pass
    except Exception as e:
        await ws.send_text(json.dumps({"event":"tool.error","data":{"message":str(e)}}))
    finally:
        await ws.close()
