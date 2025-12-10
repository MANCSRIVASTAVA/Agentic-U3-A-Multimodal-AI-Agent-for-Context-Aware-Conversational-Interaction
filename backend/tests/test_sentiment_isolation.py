"""
Sentiment service isolation tests.
"""
import pytest
import sys
from pathlib import Path
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock

# Add backend to path
backend_dir = Path(__file__).parent.parent
sys.path.insert(0, str(backend_dir))

class TestSentimentIsolation:
    """Isolation tests for Sentiment service."""
    
    def test_sentiment_health(self):
        """Test sentiment health endpoint."""
        sentiment_dir = backend_dir / "sentiment"
        sys.path.insert(0, str(sentiment_dir))
        
        with patch.dict('sys.modules', {
            'transformers': MagicMock(),
            'torch': MagicMock(),
            'numpy': MagicMock(),
        }):
            from app.main import app
            client = TestClient(app)
            
            response = client.get("/v1/health")
            assert response.status_code == 200
            data = response.json()
            assert data["status"] == "ok"
            print("PASS: Sentiment health test passed")