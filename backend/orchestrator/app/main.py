import sys
from pathlib import Path

import sys
#sys.path.append(".")

from fastapi import FastAPI, Request

from .config import settings
from .logging import RequestContextMiddleware
from .middleware import add_cors, auth_hook
from .routes import (
    health,
    config as cfg,
    metrics,
    chat_ws,
    chat_sse,   # legacy SSE route (kept for backward compatibility)
    ingest,
    retrieve,
    tts,
)
# NEW chat HTTP router (POST /v1/chat, GET /v1/chat/stream)
# Ensure you added app/routes/chat.py to your project.
from .routes import chat  # <-- add this import


def _maybe_add_repo_root_to_path():
    """Add repo root to sys.path if it contains shared/ (safe in containers)."""
    import sys
    from pathlib import Path
    here = Path(__file__).resolve()
    for pth in [here.parent, *here.parents, Path('/app')]:
        try:
            if (pth / 'shared').exists() and str(pth) not in sys.path:
                sys.path.insert(0, str(pth))
                return
        except Exception:
            pass


def create_app() -> FastAPI:
    _maybe_add_repo_root_to_path()

    app = FastAPI(title="Orchestrator", version="1.0.0")

    # CORS + request context middleware (correlation IDs, etc.)
    add_cors(app)
    app.add_middleware(RequestContextMiddleware)

    # Core routes
    app.include_router(health.router)
    app.include_router(cfg.router, dependencies=[])
    app.include_router(metrics.router)

    # Chat routes
    app.include_router(chat.router)      # <-- NEW: /v1/chat (sync) + /v1/chat/stream (SSE)
    app.include_router(chat_ws.router)   # WebSocket echo/compat
    app.include_router(chat_sse.router)  # Legacy SSE (kept to avoid breaking older clients)

    # Tooling / proxy routes
    app.include_router(ingest.router, dependencies=[])
    app.include_router(retrieve.router, dependencies=[])
    app.include_router(tts.router, dependencies=[])

    # Simple auth middleware (skips health & metrics)
    @app.middleware("http")
    async def auth_mw(request: Request, call_next):
        if request.url.path not in ["/v1/health", "/v1/metrics", "/v1/config" , "/v1/chat/sse", "/v1/chat/stream", "/v1/chat", "/docs", "/openapi.json", "/redoc" ]:
            await auth_hook(request)
        return await call_next(request)

    return app




# Expose FastAPI instance for Uvicorn
app = create_app()
