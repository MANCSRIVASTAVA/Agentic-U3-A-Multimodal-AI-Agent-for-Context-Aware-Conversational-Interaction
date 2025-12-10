# Sentiment Service (Text Sentiment + Emotion + Style Adapter)

A FastAPI microservice that analyzes **text** (and is future-ready for **audio prosody**) to infer
sentiment and emotion, then returns **style directives** that downstream LLM/TTS can use for
adaptive responses.

## Endpoints
- `GET /v1/health` — liveness/readiness probe.
- `GET /v1/metrics` — Prometheus exposition format.
- `POST /v1/analyze` — analyze text (and optionally prosody later).

### Request (JSON)
```json
{ "text": "I already tried this and it didn't work.", "features": ["sentiment","emotion"], "return_style": true }
```

### Response (JSON)
```json
{
  "sentiment": "negative",
  "emotion": "anger",
  "valence": -0.72,
  "arousal": 0.81,
  "confidence": 0.88,
  "style_directives": {
    "style_enum": "calm",
    "system_instructions": "Acknowledge frustration, be polite, concise, propose one actionable step."
  },
  "meta": { "model": "textmini/emomini", "latency_ms": 23 }
}
```

## Quickstart (Local)
```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

**Smoke tests**
```bash
curl -s http://localhost:8000/v1/health
curl -s http://localhost:8000/v1/metrics | head
curl -s -X POST http://localhost:8000/v1/analyze          -H "Content-Type: application/json"          -d '{"text":"I already tried this and it did not work."}'
```

## Docker
```bash
docker build -t sentiment:local .
docker run --rm -p 8700:8000 --env-file .env.example sentiment:local
```

## Notes
- Prosody is **optional**. If later enabled, call with `{ "text": "...", "prosody": {...} }` or provide `audio_url` (Thin STT).
- Fully offline, no paid APIs. Deterministic, seed-based heuristics to ease unit testing.
