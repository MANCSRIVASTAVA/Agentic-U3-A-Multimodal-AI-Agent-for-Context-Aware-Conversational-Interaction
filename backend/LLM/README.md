
# Agentic LLM Service (OpenAI primary, HF/TGI fallback)

This stack runs a private `llm-service` with SSE token streaming. Orchestrator (not included here) should call it.

## Quick start

1) Edit `llm/.env` and set `OPENAI_API_KEY`.
2) Run:
```bash
docker compose up -d --build
curl -s http://127.0.0.1:8200/v1/health
```
3) Test stream:
```bash
curl -N -X POST http://127.0.0.1:8200/v1/generate \
  -H "Content-Type: application/json" \
  -d '{"messages":[{"role":"system","content":"You are concise."},{"role":"user","content":"Say hi in 5 words."}],
       "stream":true,
       "max_tokens":64,
       "metadata":{"session_id":"s1","correlation_id":"c1"}}'
```

## Notes
- Primary provider: OpenAI Chat Completions (`OPENAI_*`). Fallback: Hugging Face TGI (`HF_*`).
- First token SLA: `FIRST_TOKEN_SLA_MS` (default 1000ms). Stall detection: `STALL_TIMEOUT_SEC` (default 2s).
- Metrics: `GET /v1/metrics` (Prometheus text).
- Tracing: Exported to OTLP if `OTEL_EXPORTER_OTLP_ENDPOINT` is set.
