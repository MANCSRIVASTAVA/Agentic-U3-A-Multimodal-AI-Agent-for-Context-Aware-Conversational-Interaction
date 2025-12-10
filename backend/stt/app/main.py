import json,time,os
from fastapi import FastAPI,WebSocket,WebSocketDisconnect,Response
from fastapi.responses import PlainTextResponse
from fastapi.middleware.cors import CORSMiddleware
from prometheus_client import generate_latest,CONTENT_TYPE_LATEST
from .engine import StreamingSTTEngine,EngineConfig

app=FastAPI(title="STT Service Enriched",version="1.0")

app.add_middleware(CORSMiddleware,allow_origins=["*"],allow_methods=["*"],allow_headers=["*"])

@app.get("/v1/health")
def health(): return {"ok":True,"service":"stt","time":time.time()}

@app.get("/v1/config")
def config(): return {"sample_rate":16000,"first_partial_sla_ms":800}

@app.get("/v1/metrics")
def metrics(): return Response(content=generate_latest(),media_type=CONTENT_TYPE_LATEST)

@app.websocket("/v1/transcribe/ws")
async def ws_api(ws:WebSocket):
    await ws.accept()
    cfg=EngineConfig();engine=StreamingSTTEngine(cfg)
    try:
        while True:
            msg=await ws.receive()
            if "bytes" in msg and msg["bytes"]:
                for ev,payload in engine.iter_events():
                    await ws.send_text(json.dumps({"event":ev,**payload}))
            elif "text" in msg and msg["text"]:
                data=json.loads(msg["text"]);ev=data.get("event")
                if ev=="close":
                    engine.close();break
                elif ev=="ping":
                    await ws.send_text(json.dumps({"event":"pong","ts":time.time()}))
    except WebSocketDisconnect:
        engine.close()
