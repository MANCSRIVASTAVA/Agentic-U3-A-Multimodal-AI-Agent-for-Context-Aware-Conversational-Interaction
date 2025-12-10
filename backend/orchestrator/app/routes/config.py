from fastapi import APIRouter
from pydantic import BaseModel
from ..config import settings

router = APIRouter()

class Downstreams(BaseModel):
    rag: str | None = str(settings.RAG_URL) if settings.RAG_URL else None
    llm: str | None = str(settings.LLM_URL) if settings.LLM_URL else None
    stt: str | None = str(settings.STT_URL) if settings.STT_URL else None
    tts: str | None = str(settings.TTS_URL) if settings.TTS_URL else None
    analytics: str | None = str(settings.ANALYTICS_URL) if settings.ANALYTICS_URL else None

class ConfigResponse(BaseModel):
    service: str = "orchestrator"
    port: int | None = int(settings.PORT) if settings.PORT else None
    downstreams: Downstreams

@router.get("/v1/config", response_model=ConfigResponse)
async def get_config() -> ConfigResponse:
    return ConfigResponse(downstreams=Downstreams())
