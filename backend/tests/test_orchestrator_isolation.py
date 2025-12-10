"""
Orchestrator service isolation tests.
"""
import pytest
import sys
from pathlib import Path
from fastapi.testclient import TestClient

# Add backend to path
backend_dir = Path(__file__).parent.parent
sys.path.insert(0, str(backend_dir))

class TestOrchestratorIsolation:
    """Isolation tests for Orchestrator service."""
    
    def test_orchestrator_health(self):
        """Test orchestrator health endpoint."""
        from orchestrator.app.main import create_app
        app = create_app()
        client = TestClient(app)
        
        response = client.get("/v1/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "ok"
        print("PASS: Orchestrator health test passed")
    
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
        print("PASS: Orchestrator config test passed")
    
    def test_orchestrator_metrics(self):
        """Test orchestrator metrics endpoint."""
        from orchestrator.app.main import create_app
        app = create_app()
        client = TestClient(app)
        
        response = client.get("/v1/metrics")
        assert response.status_code == 200
        assert "text/plain" in response.headers["content-type"]
        print("PASS: Orchestrator metrics test passed")