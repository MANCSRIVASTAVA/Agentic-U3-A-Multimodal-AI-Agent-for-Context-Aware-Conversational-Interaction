"""
RAG service isolation tests.
"""
import pytest
import sys
from pathlib import Path
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock

# Add backend to path
backend_dir = Path(__file__).parent.parent
sys.path.insert(0, str(backend_dir))

class TestRAGIsolation:
    """Isolation tests for RAG service."""
    
    def test_rag_health(self):
        """Test RAG health endpoint."""
        with patch.dict('sys.modules', {
            'minio': MagicMock(),
            'minio.error': MagicMock(),
            'qdrant_client': MagicMock(),
            'qdrant_client.http': MagicMock(),
            'qdrant_client.models': MagicMock(),
        }):
            from rag.app.main import app
            client = TestClient(app)
            
            response = client.get("/v1/health")
            assert response.status_code == 200
            data = response.json()
            assert data["status"] == "ok"
            print("PASS: RAG health test passed")