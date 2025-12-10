import os
from pydantic import BaseSettings

class Settings(BaseSettings):
    SERVICE_NAME: str = "feedback"
    SERVICE_PORT: int = int(os.getenv("PORT", 8000))

    ORCHESTRATOR_HOST: str = os.getenv("ORCHESTRATOR_HOST", "localhost")
    ORCHESTRATOR_HOST_PORT: int = int(os.getenv("ORCHESTRATOR_HOST_PORT", "8081"))
    LLM_HOST: str = os.getenv("LLM_HOST", "localhost")
    LLM_HOST_PORT: int = int(os.getenv("LLM_HOST_PORT", "8200"))

    POSTGRES_DSN: str = os.getenv(
        "POSTGRES_DSN",
        f"postgresql+asyncpg://postgres:postgres@localhost:{os.getenv('POSTGRES_PORT','5432')}/agentic",
    )
    REDIS_URL: str = os.getenv("REDIS_URL", f"redis://localhost:{os.getenv('REDIS_PORT','6379')}/0")
    CLICKHOUSE_URL: str = os.getenv("CLICKHOUSE_URL", f"http://localhost:{os.getenv('CLICKHOUSE_HTTP_PORT','8123')}")
    CLICKHOUSE_USER: str = os.getenv("CLICKHOUSE_USER", "default")
    CLICKHOUSE_PASSWORD: str = os.getenv("CLICKHOUSE_PASSWORD", "")

    MINIO_ENDPOINT: str = os.getenv("MINIO_ENDPOINT", f"localhost:{os.getenv('MINIO_API_PORT','9000')}")
    MINIO_ACCESS_KEY: str = os.getenv("MINIO_ACCESS_KEY", "minioadmin")
    MINIO_SECRET_KEY: str = os.getenv("MINIO_SECRET_KEY", "minioadmin")
    MINIO_SECURE: bool = os.getenv("MINIO_SECURE", "false").lower() == "true"
    MINIO_BUCKET_REPORTS: str = os.getenv("MINIO_BUCKET_REPORTS", "feedback-reports")

    REDIS_STREAM_SESSION_COMPLETED: str = os.getenv("REDIS_STREAM_SESSION_COMPLETED", "session.completed")
    REQUIRE_AUDIO_CONSENT: bool = os.getenv("REQUIRE_AUDIO_CONSENT", "true").lower() == "true"

settings = Settings()
