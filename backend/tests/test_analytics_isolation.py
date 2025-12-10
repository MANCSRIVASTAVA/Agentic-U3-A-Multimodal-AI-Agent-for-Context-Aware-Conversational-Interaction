"""
Analytics service isolation tests.
"""
import pytest
import sys
from pathlib import Path
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock

# Add backend to path
backend_dir = Path(__file__).parent.parent
sys.path.insert(0, str(backend_dir))

class TestAnalyticsIsolation:
    """Isolation tests for Analytics service."""
    
    def test_analytics_health(self):
        """Test analytics health endpoint."""
        with patch.dict('sys.modules', {'clickhouse_driver': MagicMock()}):
            from analytics.app.main import app
            client = TestClient(app)
            
            response = client.get("/v1/health")
            assert response.status_code == 200
            data = response.json()
            assert data["status"] == "ok"
            assert data["service"] == "analytics"
            print("PASS: Analytics health test passed")
    
    def test_analytics_config(self):
        """Test analytics config endpoint."""
        with patch.dict('sys.modules', {'clickhouse_driver': MagicMock()}):
            from analytics.app.main import app
            client = TestClient(app)
            
            response = client.get("/v1/config")
            assert response.status_code == 200
            data = response.json()
            assert "CLICKHOUSE_HOST" in data
            print("PASS: Analytics config test passed")
    
    def test_analytics_metrics(self):
        """Test analytics metrics endpoint."""
        with patch.dict('sys.modules', {'clickhouse_driver': MagicMock()}):
            from analytics.app.main import app
            client = TestClient(app)
            
            response = client.get("/v1/metrics")
            assert response.status_code == 200
            assert "text/plain" in response.headers["content-type"]
            print("PASS: Analytics metrics test passed")