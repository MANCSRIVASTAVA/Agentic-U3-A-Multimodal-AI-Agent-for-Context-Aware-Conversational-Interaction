"""
LLM service isolation tests.
"""
import pytest
import sys
from pathlib import Path
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock

# Add backend to path
backend_dir = Path(__file__).parent.parent
sys.path.insert(0, str(backend_dir))

class TestLLMIsolation:
    """Isolation tests for LLM service."""
    
    def test_llm_health(self):
        """Test LLM health endpoint."""
        llm_dir = backend_dir / "LLM"
        sys.path.insert(0, str(llm_dir))
        
        with patch.dict('sys.modules', {
            'openai': MagicMock(),
            'transformers': MagicMock(),
            'torch': MagicMock(),
        }):
            from app.main import app
            client = TestClient(app)
            
            response = client.get("/v1/health")
            assert response.status_code == 200
            data = response.json()
            assert data["status"] == "ok"
            print("PASS: LLM health test passed")
    
    def test_llm_metrics(self):
        """Test LLM metrics endpoint."""
        llm_dir = backend_dir / "LLM"
        sys.path.insert(0, str(llm_dir))
        
        with patch.dict('sys.modules', {
            'openai': MagicMock(),
            'transformers': MagicMock(),
            'torch': MagicMock(),
        }):
            from app.main import app
            client = TestClient(app)
            
            response = client.get("/v1/metrics")
            assert response.status_code == 200
            assert "text/plain" in response.headers["content-type"]
            print("PASS: LLM metrics test passed")