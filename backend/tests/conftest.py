"""
Shared test configuration and fixtures for microservice isolation testing.
"""
import os
import pytest
import asyncio
import httpx
from typing import Dict, Any, Optional
from unittest.mock import Mock, patch
from fastapi.testclient import TestClient
from contextlib import asynccontextmanager
import json
import time
from datetime import datetime, timezone

# Test configuration
TEST_CONFIG = {
    "services": {
        "orchestrator": {"port": 8000, "health_path": "/v1/health"},
        "analytics": {"port": 8090, "health_path": "/v1/health"},
        "llm": {"port": 8012, "health_path": "/v1/health"},
        "rag": {"port": 8011, "health_path": "/v1/health"},
        "sentiment": {"port": 8013, "health_path": "/v1/health"},
        "stt": {"port": 8014, "health_path": "/v1/health"},
        "tts": {"port": 8015, "health_path": "/v1/health"},
        "feedback": {"port": 8016, "health_path": "/v1/health"},
    },
    "test_timeout": 30,
    "mock_external_services": True,
}

@pytest.fixture(scope="session")
def event_loop():
    """Create an instance of the default event loop for the test session."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()

@pytest.fixture(scope="session")
def test_config():
    """Provide test configuration."""
    return TEST_CONFIG

@pytest.fixture
def mock_environment():
    """Mock environment variables for testing."""
    env_vars = {
        "AUTH_TOKEN": "test-token",
        "RAG_URL": "http://localhost:8011",
        "LLM_URL": "http://localhost:8012",
        "ANALYTICS_URL": "http://localhost:8090",
        "SENTIMENT_URL": "http://localhost:8013",
        "STT_URL": "http://localhost:8014",
        "TTS_URL": "http://localhost:8015",
        "FEEDBACK_URL": "http://localhost:8016",
        "CLICKHOUSE_HOST": "localhost",
        "CLICKHOUSE_PORT": "9000",
        "CLICKHOUSE_DB": "test_analytics",
        "REDIS_URL": "redis://localhost:6379",
        "POSTGRES_URL": "postgresql://test:test@localhost:5432/test",
        "QDRANT_URL": "http://localhost:6333",
        "MINIO_URL": "http://localhost:9000",
        "MINIO_ACCESS_KEY": "test",
        "MINIO_SECRET_KEY": "test123",
    }
    
    with patch.dict(os.environ, env_vars):
        yield env_vars

@pytest.fixture
def mock_http_client():
    """Mock HTTP client for external service calls."""
    mock_client = Mock(spec=httpx.AsyncClient)
    return mock_client

@pytest.fixture
def mock_database():
    """Mock database connections."""
    mock_db = Mock()
    mock_db.execute = Mock(return_value=Mock())
    mock_db.fetchall = Mock(return_value=[])
    mock_db.fetchone = Mock(return_value=None)
    return mock_db

@pytest.fixture
def mock_redis():
    """Mock Redis client."""
    mock_redis = Mock()
    mock_redis.get = Mock(return_value=None)
    mock_redis.set = Mock(return_value=True)
    mock_redis.delete = Mock(return_value=1)
    mock_redis.exists = Mock(return_value=False)
    return mock_redis

@pytest.fixture
def mock_clickhouse():
    """Mock ClickHouse client."""
    mock_ch = Mock()
    mock_ch.execute = Mock(return_value=[])
    mock_ch.insert = Mock(return_value=True)
    mock_ch.query = Mock(return_value=[])
    return mock_ch

@pytest.fixture
def mock_qdrant():
    """Mock Qdrant client."""
    mock_qdrant = Mock()
    mock_qdrant.search = Mock(return_value=[])
    mock_qdrant.upsert = Mock(return_value=True)
    mock_qdrant.delete = Mock(return_value=True)
    return mock_qdrant

@pytest.fixture
def mock_minio():
    """Mock MinIO client."""
    mock_minio = Mock()
    mock_minio.put_object = Mock(return_value=True)
    mock_minio.get_object = Mock(return_value=b"test data")
    mock_minio.remove_object = Mock(return_value=True)
    return mock_minio

@pytest.fixture
def sample_events():
    """Sample events for testing analytics service."""
    return [
        {
            "session_id": "test-session-1",
            "correlation_id": "test-correlation-1",
            "type": "llm_start",
            "ts": datetime.now(timezone.utc).isoformat(),
            "latencies": {"first_token_ms": 150.0},
            "usage": {"prompt_tokens": 10, "completion_tokens": 5},
            "flags": {"fallback_used": 0},
            "labels": {"provider": "openai", "model": "gpt-4o"}
        },
        {
            "session_id": "test-session-1",
            "correlation_id": "test-correlation-1",
            "type": "llm_done",
            "ts": datetime.now(timezone.utc).isoformat(),
            "latencies": {"total_ms": 500.0},
            "usage": {"prompt_tokens": 10, "completion_tokens": 5},
            "flags": {"fallback_used": 0},
            "labels": {"provider": "openai", "model": "gpt-4o"}
        }
    ]

@pytest.fixture
def sample_rag_response():
    """Sample RAG response for testing."""
    return {
        "results": [
            {
                "text": "Sample document chunk 1",
                "score": 0.95,
                "source_url": "minio://test-bucket/doc1#1",
                "doc_id": "doc1",
                "chunk_id": "1"
            },
            {
                "text": "Sample document chunk 2",
                "score": 0.88,
                "source_url": "minio://test-bucket/doc2#2",
                "doc_id": "doc2",
                "chunk_id": "2"
            }
        ]
    }

@pytest.fixture
def sample_llm_response():
    """Sample LLM response for testing."""
    return {
        "provider": "openai",
        "model": "gpt-4o",
        "output": "This is a test response from the LLM service.",
        "fallback_used": False
    }

@pytest.fixture
def sample_sentiment_response():
    """Sample sentiment analysis response."""
    return {
        "text_sentiment": {
            "label": "positive",
            "confidence": 0.95,
            "valence": 0.8
        },
        "emotion": {
            "label": "joy",
            "confidence": 0.88,
            "arousal": 0.7
        }
    }

@pytest.fixture
def sample_stt_response():
    """Sample STT response."""
    return {
        "text": "This is a test transcription",
        "confidence": 0.95,
        "language": "en",
        "duration": 2.5
    }

@pytest.fixture
def sample_tts_response():
    """Sample TTS response."""
    return {
        "audio_url": "minio://test-bucket/audio/test-audio.wav",
        "duration": 2.5,
        "format": "wav",
        "sample_rate": 22050
    }

class MockServiceClient:
    """Mock client for simulating other microservices."""
    
    def __init__(self, service_name: str):
        self.service_name = service_name
        self.responses = {}
        self.call_count = 0
    
    def set_response(self, endpoint: str, response: Dict[str, Any], status_code: int = 200):
        """Set a mock response for an endpoint."""
        self.responses[endpoint] = {
            "data": response,
            "status_code": status_code
        }
    
    async def get(self, url: str, **kwargs):
        """Mock GET request."""
        self.call_count += 1
        endpoint = url.split("/")[-1] if "/" in url else url
        
        if endpoint in self.responses:
            response_data = self.responses[endpoint]
            return Mock(
                status_code=response_data["status_code"],
                json=lambda: response_data["data"],
                text=json.dumps(response_data["data"])
            )
        
        # Default response
        return Mock(
            status_code=200,
            json=lambda: {"status": "ok", "service": self.service_name},
            text='{"status": "ok", "service": "' + self.service_name + '"}'
        )
    
    async def post(self, url: str, json=None, **kwargs):
        """Mock POST request."""
        self.call_count += 1
        endpoint = url.split("/")[-1] if "/" in url else url
        
        if endpoint in self.responses:
            response_data = self.responses[endpoint]
            return Mock(
                status_code=response_data["status_code"],
                json=lambda: response_data["data"],
                text=json.dumps(response_data["data"])
            )
        
        # Default response
        return Mock(
            status_code=200,
            json=lambda: {"status": "ok", "service": self.service_name},
            text='{"status": "ok", "service": "' + self.service_name + '"}'
        )

@pytest.fixture
def mock_rag_client(sample_rag_response):
    """Mock RAG service client."""
    client = MockServiceClient("rag")
    client.set_response("retrieve", sample_rag_response)
    client.set_response("health", {"status": "ok", "service": "rag"})
    return client

@pytest.fixture
def mock_llm_client(sample_llm_response):
    """Mock LLM service client."""
    client = MockServiceClient("llm")
    client.set_response("generate", sample_llm_response)
    client.set_response("health", {"status": "ok", "service": "llm"})
    return client

@pytest.fixture
def mock_analytics_client():
    """Mock Analytics service client."""
    client = MockServiceClient("analytics")
    client.set_response("ingest", {"status": "ok", "event_id": "test-event-id"})
    client.set_response("health", {"status": "ok", "service": "analytics"})
    return client

@pytest.fixture
def mock_sentiment_client(sample_sentiment_response):
    """Mock Sentiment service client."""
    client = MockServiceClient("sentiment")
    client.set_response("analyze", sample_sentiment_response)
    client.set_response("health", {"status": "ok", "service": "sentiment"})
    return client

@pytest.fixture
def mock_stt_client(sample_stt_response):
    """Mock STT service client."""
    client = MockServiceClient("stt")
    client.set_response("transcribe", sample_stt_response)
    client.set_response("health", {"status": "ok", "service": "stt"})
    return client

@pytest.fixture
def mock_tts_client(sample_tts_response):
    """Mock TTS service client."""
    client = MockServiceClient("tts")
    client.set_response("synthesize", sample_tts_response)
    client.set_response("health", {"status": "ok", "service": "tts"})
    return client

@pytest.fixture
def mock_feedback_client():
    """Mock Feedback service client."""
    client = MockServiceClient("feedback")
    client.set_response("process", {"status": "ok", "feedback_id": "test-feedback-id"})
    client.set_response("health", {"status": "ok", "service": "feedback"})
    return client

def create_test_app(service_module, app_factory_name="app"):
    """Helper to create test app instances."""
    try:
        if hasattr(service_module, app_factory_name):
            return getattr(service_module, app_factory_name)
        elif hasattr(service_module, "create_app"):
            return service_module.create_app()
        else:
            raise AttributeError(f"No app factory found in {service_module}")
    except Exception as e:
        pytest.skip(f"Could not create test app: {e}")

@pytest.fixture
def test_client_factory():
    """Factory for creating test clients."""
    def _create_client(service_module, app_factory_name="app"):
        app = create_test_app(service_module, app_factory_name)
        return TestClient(app)
    return _create_client
