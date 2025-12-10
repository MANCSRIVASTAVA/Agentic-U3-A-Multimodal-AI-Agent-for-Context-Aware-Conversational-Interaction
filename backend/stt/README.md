# STT Service (Enriched Phase 6)

- WS /v1/transcribe/ws supports session_id, correlation_id, segment_id, language.
- Emits transcript.final, transcript.error, warning(backpressure), pong(ping).

## Quickstart
pip install -r stt/requirements.txt
uvicorn app.main:app --app-dir stt --host 0.0.0.0 --port 8000
