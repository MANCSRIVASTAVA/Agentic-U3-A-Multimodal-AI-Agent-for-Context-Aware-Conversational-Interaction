
import os
import time
import logging
from typing import Dict, Any

from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import PlainTextResponse

from prometheus_client import (
    CONTENT_TYPE_LATEST,
    CollectorRegistry,
    generate_latest,
    Counter,
    Histogram,
)

try:
    from shared.middleware import with_correlation_id  # type: ignore
except Exception:
    def with_correlation_id(app: FastAPI):
        @app.middleware("http")
        async def _mw(request: Request, call_next):
            cid = request.headers.get("X-Correlation-Id") or request.headers.get("X-Request-Id")
            if not cid:
                cid = str(int(time.time() * 1000))
            request.state.correlation_id = cid
            response: Response = await call_next(request)
            response.headers["X-Correlation-Id"] = cid
            return response
        return app

from .minio_client import MinioStore
from .qdrant_client import QdrantStore
from .embedder import Embedder
from .ingest import router as ingest_router
from .retrieve import router as retrieve_router

SERVICE_NAME = os.getenv("SERVICE_NAME", "rag")
PORT = int(os.getenv("PORT", "8000"))

# ---- Logging ----
logger = logging.getLogger(SERVICE_NAME)
logging.basicConfig(level=os.getenv("LOG_LEVEL", "INFO"))

# ---- Metrics ----
registry = CollectorRegistry()
INGEST_DURATION = Histogram(
    "rag_ingest_duration_seconds", "Time spent ingesting a document", registry=registry
)
EMBED_LATENCY = Histogram(
    "rag_embed_latency_seconds", "Embedding latency per batch", registry=registry
)
ANN_LATENCY = Histogram(
    "rag_ann_latency_seconds", "Vector search latency", registry=registry
)
CHUNKS_INGESTED = Counter(
    "rag_chunks_ingested_total", "Total chunks ingested", registry=registry
)


def build_app() -> FastAPI:
    app = FastAPI(title="RAG Service", version="1.0.0")

    # CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    with_correlation_id(app)

    # Shared state (clients + embedder)
    @app.on_event("startup")
    async def _startup():
        logger.info("[startup] initializing clients and embedder")
        app.state.minio = MinioStore(
            endpoint=os.getenv("MINIO_ENDPOINT", "http://minio:9000"),
            access_key=os.getenv("MINIO_ACCESS_KEY", "minioadmin"),
            secret_key=os.getenv("MINIO_SECRET_KEY", "minioadmin"),
            secure=os.getenv("MINIO_SECURE", "false").lower() == "true",
            bucket=os.getenv("MINIO_BUCKET", "app-bucket"),
            presign_days=int(os.getenv("MINIO_PRESIGN_DAYS", "7")),
        )
        app.state.embedder = Embedder(model_name=os.getenv(
            "EMBED_MODEL", "sentence-transformers/all-MiniLM-L6-v2"))
        app.state.qdrant = QdrantStore(
            url=os.getenv("QDRANT_URL", "http://qdrant:6333"),
            api_key=os.getenv("QDRANT_API_KEY"),
            collection=os.getenv("QDRANT_COLLECTION", "rag_chunks"),
            vector_size=app.state.embedder.dim,
        )
        logger.info("[startup] ready")

    @app.get("/v1/health")
    async def health(deep: int = 0):
        data: Dict[str, Any] = {"status": "ok", "service": SERVICE_NAME}
        if deep:
            data.update({
                "minio_bucket": app.state.minio.bucket,
                "qdrant_collection": app.state.qdrant.collection,
                "embed_model": app.state.embedder.model_name,
                "embed_dim": app.state.embedder.dim,
            })
        return data

    @app.get("/v1/config")
    async def config():
        return {
            "service": SERVICE_NAME,
            "minio": {"endpoint": os.getenv("MINIO_ENDPOINT"), "bucket": app.state.minio.bucket},
            "qdrant": {"url": os.getenv("QDRANT_URL"), "collection": app.state.qdrant.collection},
            "embed_model": app.state.embedder.model_name,
        }

    @app.get("/v1/metrics")
    async def metrics():
        return PlainTextResponse(generate_latest(registry), media_type=CONTENT_TYPE_LATEST)

    # Routers (pass metrics to modules via app.state)
    app.include_router(ingest_router, prefix="/v1", tags=["ingest"])
    app.include_router(retrieve_router, prefix="/v1", tags=["retrieve"])

    # Expose metrics objects for modules
    app.state.metrics = {
        "INGEST_DURATION": INGEST_DURATION,
        "EMBED_LATENCY": EMBED_LATENCY,
        "ANN_LATENCY": ANN_LATENCY,
        "CHUNKS_INGESTED": CHUNKS_INGESTED,
    }

    return app


app = build_app()
