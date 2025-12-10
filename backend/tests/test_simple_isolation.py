"""
Simplified isolation tests for microservices.

These tests focus on basic functionality without complex mocking.
"""
import pytest
import sys
from pathlib import Path
from fastapi.testclient import TestClient

# Add backend to path
backend_dir = Path(__file__).parent.parent
sys.path.insert(0, str(backend_dir))

class TestSimpleIsolation:
    """Simple isolation tests that focus on basic functionality."""
    
    def test_orchestrator_health(self):
        """Test orchestrator health endpoint."""
        from orchestrator.app.main import create_app
        
        app = create_app()
        client = TestClient(app)
        
        response = client.get("/v1/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "ok"
    
    def test_orchestrator_config(self):
        """Test orchestrator config endpoint."""
        from orchestrator.app.main import create_app
        
        app = create_app()
        client = TestClient(app)
        
        response = client.get("/v1/config")
        assert response.status_code == 200
        data = response.json()
        assert "service" in data
        assert data["service"] == "orchestrator"
    
    def test_orchestrator_metrics(self):
        """Test orchestrator metrics endpoint."""
        from orchestrator.app.main import create_app
        
        app = create_app()
        client = TestClient(app)
        
        response = client.get("/v1/metrics")
        assert response.status_code == 200
        assert "text/plain" in response.headers["content-type"]
    
    def test_analytics_health(self):
        """Test analytics health endpoint."""
        from analytics.app.main import app
        
        client = TestClient(app)
        
        response = client.get("/v1/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "ok"
        assert data["service"] == "analytics"
    
    def test_analytics_config(self):
        """Test analytics config endpoint."""
        from analytics.app.main import app
        
        client = TestClient(app)
        
        response = client.get("/v1/config")
        assert response.status_code == 200
        data = response.json()
        assert "CLICKHOUSE_HOST" in data
    
    def test_llm_health(self):
        """Test LLM health endpoint."""
        from LLM.app.main import app
        
        client = TestClient(app)
        
        response = client.get("/v1/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "ok"
    
    def test_llm_metrics(self):
        """Test LLM metrics endpoint."""
        from LLM.app.main import app
        
        client = TestClient(app)
        
        response = client.get("/v1/metrics")
        assert response.status_code == 200
        assert "text/plain" in response.headers["content-type"]
    
    def test_sentiment_health(self):
        """Test sentiment health endpoint."""
        from sentiment.app.main import app
        
        client = TestClient(app)
        
        response = client.get("/v1/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "ok"
    
    def test_stt_health(self):
        """Test STT health endpoint."""
        from stt.app.main import app
        
        client = TestClient(app)
        
        response = client.get("/v1/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "ok"
    
    def test_tts_health(self):
        """Test TTS health endpoint."""
        from tts.app.main import app
        
        client = TestClient(app)
        
        response = client.get("/v1/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "ok"
    
    def test_rag_health(self):
        """Test RAG health endpoint."""
        from rag.app.main import app
        
        client = TestClient(app)
        
        response = client.get("/v1/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "ok"
    
    def test_feedback_health(self):
        """Test feedback health endpoint."""
        from feedback.app import app
        
        client = TestClient(app)
        
        response = client.get("/v1/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "ok"

