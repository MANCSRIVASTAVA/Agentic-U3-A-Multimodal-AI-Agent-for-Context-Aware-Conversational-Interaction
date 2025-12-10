import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1.health import router as health_router
from app.api.v1.metrics import router as metrics_router
from app.api.v1.analyze import router as analyze_router
from app.core.config import settings

logger = logging.getLogger("sentiment.main")

app = FastAPI(title="Sentiment Service", version="1.0.0")

allow_origins = settings.cors_allow_origins.split(",") if settings.cors_allow_origins else ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=allow_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health_router, prefix="/v1")
app.include_router(metrics_router, prefix="/v1")
app.include_router(analyze_router, prefix="/v1")

@app.get("/")
def root():
    return {"service": "sentiment", "status": "ok"}
