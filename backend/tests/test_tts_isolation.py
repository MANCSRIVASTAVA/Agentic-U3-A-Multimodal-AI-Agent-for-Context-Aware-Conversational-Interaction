"""
TTS service isolation tests.
"""
import pytest
import sys
from pathlib import Path
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock

# Add backend to path
backend_dir = Path(__file__).parent.parent
sys.path.insert(0, str(backend_dir))

class TestTTSIsolation:
    """Isolation tests for TTS service."""
    
    def test_tts_health(self):
        """Test TTS health endpoint."""
        with patch.dict('sys.modules', {
            'torch': MagicMock(),
            'torchaudio': MagicMock(),
            'TTS': MagicMock(),
        }):
            from tts.app.main import app
            client = TestClient(app)
            
            response = client.get("/v1/health")
            assert response.status_code == 200
            data = response.json()
            assert data["status"] == "ok"
            print("PASS: TTS health test passed")
    
    def test_tts_metrics(self):
        """Test TTS metrics endpoint."""
        with patch.dict('sys.modules', {
            'torch': MagicMock(),
            'torchaudio': MagicMock(),
            'TTS': MagicMock(),
        }):
            from tts.app.main import app
            client = TestClient(app)
            
            response = client.get("/v1/metrics")
            assert response.status_code == 200
            assert "text/plain" in response.headers["content-type"]
            print("PASS: TTS metrics test passed")