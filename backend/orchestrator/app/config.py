from pydantic_settings import BaseSettings
from pydantic import Field
from typing import Optional

class Settings(BaseSettings):
    # Service runtime
    PORT: int = 8000
    AUTH_TOKEN: str = "devtoken"

    # Core infra
    REDIS_URL: str = "redis://redis:6379/0"
    POSTGRES_DSN: str = "postgresql://user:pass@postgres:5432/agentic"

    # Upstreams (internal service mesh URLs)
    RAG_URL: str = "http://rag:8011"
    LLM_URL: str = "http://llm:8012"
    STT_URL: str = "ws://stt:8010"
    TTS_URL: str = "http://tts:8013"
    ANALYTICS_URL: str = "http://analytics:8090"

    # Orchestrator chat behavior
    RAG_AUTO_LENGTH_THRESHOLD: int = Field(
        120,
        description="Auto-enable RAG if query length ≥ this threshold unless use_rag is explicitly set."
    )

    # Observability / tracing
    OTEL_EXPORTER_OTLP_ENDPOINT: Optional[str] = None

    # HTTP server behavior
    CORS_ALLOW_ORIGINS: str = "*"
    REQUEST_TIMEOUT_SECONDS: float = 30.0
    RETRIES: int = 2

    class Config:
        env_file = ".env"
        extra = "allow"

settings = Settings()

