from fastapi import FastAPI, Request, Response
from fastapi.responses import StreamingResponse, JSONResponse
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST
import time, os, base64
from typing import AsyncGenerator, Optional
from pydantic import BaseModel

class TTSRequest(BaseModel):
    text: str
    voice: Optional[str] = None
    format: str = "mp3"
    correlation_id: Optional[str] = None
    session_id: Optional[str] = None

tts_requests_total = Counter('tts_requests_total', 'Total TTS requests', ['provider'])
tts_fallback_total = Counter('tts_fallback_total', 'Total TTS fallbacks', ['reason'])
tts_errors_total = Counter('tts_errors_total', 'Total TTS errors', ['code'])
tts_latency_ms = Histogram('tts_latency_ms', 'TTS latency in ms', ['provider'])

app = FastAPI(title="TTS Service", version="1.0.0")

CONFIG = {
    "default_voice": os.getenv("ELEVEN_VOICE", "female_en"),
    "request_timeout_ms": int(os.getenv("REQUEST_TIMEOUT_MS", "15000")),
    "fallback_engine": os.getenv("FALLBACK_ENGINE", "gtts"),
}

@app.get("/v1/health")
def health():
    return {"status": "ok"}

@app.get("/v1/config")
def get_config():
    return CONFIG

@app.get("/v1/metrics")
def metrics():
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)

async def sse_event(event: str, data: str):
    yield f"event: {event}\\n".encode()
    payload = data.replace("\\n", " ")
    yield f"data: {payload}\\n\\n".encode()

async def stream_audio_chunks(chunks):
    idx = 0
    async for chunk in chunks:
        b64 = base64.b64encode(chunk).decode()
        async for part in sse_event("tts.audio", f'{{"chunk":"{b64}","idx":{idx}}}'):
            yield part
        idx += 1

@app.post("/v1/tts")
async def tts_endpoint(body: TTSRequest, request: Request):
    start = time.time()
    provider = "elevenlabs"
    eleven_api_key = os.getenv("ELEVEN_API_KEY")
    try:
        from .engine import elevenlabs_stream, gtts_stream
        async def choose_and_stream():
            nonlocal provider
            try:
                if not eleven_api_key:
                    raise RuntimeError("ELEVEN_API_KEY missing")
                tts_requests_total.labels(provider=provider).inc()
                async for evt in stream_audio_chunks(elevenlabs_stream(text=body.text, voice=body.voice or CONFIG["default_voice"], fmt=body.format)):
                    yield evt
            except Exception as e:
                provider = "gtts"
                tts_fallback_total.labels(reason=type(e).__name__).inc()
                tts_requests_total.labels(provider=provider).inc()
                async for evt in stream_audio_chunks(gtts_stream(text=body.text, voice=body.voice or CONFIG["default_voice"], fmt=body.format)):
                    yield evt
            finally:
                latency_ms = int((time.time() - start) * 1000)
                tts_latency_ms.labels(provider=provider).observe(latency_ms)
                async for tail in sse_event("tts.done", f'{{"voice":"{body.voice or CONFIG["default_voice"]}","provider":"{provider}","latency_ms":{latency_ms},"fallback_used":{str(provider!="elevenlabs").lower()}}}'):
                    yield tail
        return StreamingResponse(choose_and_stream(), media_type="text/event-stream")
    except Exception as e:
        tts_errors_total.labels(code=type(e).__name__).inc()
        return JSONResponse(status_code=500, content={
            "code": "TTS_ERROR",
            "message": str(e),
            "correlation_id": body.correlation_id
        })
