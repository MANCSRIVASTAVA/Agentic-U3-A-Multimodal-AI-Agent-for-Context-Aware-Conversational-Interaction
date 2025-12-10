from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy import text
import clickhouse_connect
from minio import Minio
from .config import settings
from urllib.parse import urlparse

# Postgres (async SQLAlchemy)
engine = create_async_engine(settings.POSTGRES_DSN, pool_pre_ping=True)
SessionLocal = async_sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

async def ping_postgres():
    async with engine.connect() as conn:
        await conn.execute(text("SELECT 1"))

# ClickHouse client
parsed = urlparse(settings.CLICKHOUSE_URL)
ch_host = parsed.hostname or "localhost"
ch_port = parsed.port or 8123
ch_client = clickhouse_connect.get_client(host=ch_host, port=ch_port,
                                          username=settings.CLICKHOUSE_USER, password=settings.CLICKHOUSE_PASSWORD)

# MinIO client
minio = Minio(
    settings.MINIO_ENDPOINT,
    access_key=settings.MINIO_ACCESS_KEY,
    secret_key=settings.MINIO_SECRET_KEY,
    secure=settings.MINIO_SECURE,
)
