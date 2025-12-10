# Orchestrator (Phase 3–6) — FastAPI Entry Point

Single entrypoint for Chat (WS/SSE/HTTP), tool routing, and service proxying.
Compatible with your `shared/`, obs stack, and data stack.

---

## Run (local)

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

# Core env
export PORT=8000 AUTH_TOKEN=devtoken
export REDIS_URL=redis://localhost:6379/0
export POSTGRES_DSN=postgresql://user:pass@localhost:5432/agentic

# Upstreams (adjust if running via compose)
export RAG_URL=http://localhost:8011
export LLM_URL=http://localhost:8012
export STT_URL=ws://localhost:8010
export TTS_URL=http://localhost:8013
export ANALYTICS_URL=http://localhost:8090

# Optional behavior
export RAG_AUTO_LENGTH_THRESHOLD=120

uvicorn app.main:create_app --factory --reload --port ${PORT}

