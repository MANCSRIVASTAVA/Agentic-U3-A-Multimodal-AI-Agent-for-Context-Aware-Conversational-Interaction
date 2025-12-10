"""
STT service isolation tests.
"""
import pytest
import sys
from pathlib import Path
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock

# Add backend to path
backend_dir = Path(__file__).parent.parent
sys.path.insert(0, str(backend_dir))

class TestSTTIsolation:
    """Isolation tests for STT service."""
    
    def test_stt_health(self):
        """Test STT health endpoint."""
        with patch.dict('sys.modules', {
            'torch': MagicMock(),
            'torchaudio': MagicMock(),
            'whisper': MagicMock(),
        }):
            from stt.app.main import app
            client = TestClient(app)
            
            response = client.get("/v1/health")
            assert response.status_code == 200
            data = response.json()
            assert data["ok"] == True
            assert data["service"] == "stt"
            print("PASS: STT health test passed")
    
    def test_stt_config(self):
        """Test STT config endpoint."""
        with patch.dict('sys.modules', {
            'torch': MagicMock(),
            'torchaudio': MagicMock(),
            'whisper': MagicMock(),
        }):
            from stt.app.main import app
            client = TestClient(app)
            
            response = client.get("/v1/config")
            assert response.status_code == 200
            data = response.json()
            assert "sample_rate" in data
            print("PASS: STT config test passed")
    
    def test_stt_metrics(self):
        """Test STT metrics endpoint."""
        with patch.dict('sys.modules', {
            'torch': MagicMock(),
            'torchaudio': MagicMock(),
            'whisper': MagicMock(),
        }):
            from stt.app.main import app
            client = TestClient(app)
            
            response = client.get("/v1/metrics")
            assert response.status_code == 200
            assert "text/plain" in response.headers["content-type"]
            print("PASS: STT metrics test passed")