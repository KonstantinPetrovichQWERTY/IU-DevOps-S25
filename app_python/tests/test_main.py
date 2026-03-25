import pytest
from fastapi.testclient import TestClient
from datetime import datetime
import os
from unittest.mock import patch

from app import app

client = TestClient(app)

# ==================== ROOT ENDPOINT TESTS ====================


class TestRootEndpoint:
    """Test suite for the root endpoint (GET /)"""

    def test_root_endpoint_structure(self):
        """Test that the root endpoint returns the expected JSON structure"""
        response = client.get("/")
        assert response.status_code == 200

        data = response.json()

        # Test top-level structure
        assert "service" in data
        assert "system" in data
        assert "runtime" in data
        assert "request" in data
        assert "endpoints" in data

        # Test service section
        service = data["service"]
        assert service["name"] == "devops-info-service"
        assert service["version"] == "1.0.0"
        assert "description" in service
        assert "framework" in service
        assert service["framework"] == "FastApi"

        # Test system section
        system = data["system"]
        required_system_fields = [
            "hostname",
            "platform",
            "platform_version",
            "architecture",
            "cpu_count",
            "python_version",
        ]
        for field in required_system_fields:
            assert field in system
            assert system[field] is not None

        # Test runtime section
        runtime = data["runtime"]
        assert "uptime_seconds" in runtime
        assert "uptime_human" in runtime
        assert "current_time" in runtime
        assert "timezone" in runtime
        assert runtime["timezone"] == "UTC"

        # Test request section
        request_info = data["request"]
        assert "client_ip" in request_info
        assert "user_agent" in request_info
        assert "method" in request_info
        assert request_info["method"] == "GET"
        assert "path" in request_info
        assert request_info["path"] == "/"

        # Test endpoints section
        endpoints = data["endpoints"]
        assert isinstance(endpoints, list)
        assert len(endpoints) >= 2

        # Check for required endpoints
        endpoint_paths = [e["path"] for e in endpoints]
        assert "/" in endpoint_paths
        assert "/health" in endpoint_paths

    def test_root_endpoint_returns_valid_datetime(self):
        """Test that the current_time field contains a valid ISO datetime"""
        response = client.get("/")
        data = response.json()

        # Parse the datetime string
        current_time_str = data["runtime"]["current_time"]
        try:
            # Try parsing ISO format
            parsed_time = datetime.fromisoformat(
                current_time_str.replace("Z", "+00:00")
            )
            assert isinstance(parsed_time, datetime)
        except (ValueError, AttributeError):
            pytest.fail(f"Invalid datetime format: {current_time_str}")


# ==================== HEALTH ENDPOINT TESTS ====================


class TestHealthEndpoint:
    """Test suite for the health endpoint (GET /health)"""

    def test_health_check_success(self):
        """Test that health endpoint returns healthy status"""
        response = client.get("/health")
        assert response.status_code == 200

        data = response.json()
        assert data["status"] == "healthy"
        assert "timestamp" in data
        assert "uptime_seconds" in data

    def test_health_check_timestamp_format(self):
        """Test that timestamp is in correct format"""
        response = client.get("/health")
        data = response.json()

        timestamp = data["timestamp"]
        try:
            # Try parsing ISO format
            parsed_time = datetime.fromisoformat(
                timestamp.replace("Z", "+00:00"),
            )
            assert isinstance(parsed_time, datetime)
        except (ValueError, AttributeError):
            pytest.fail(f"Invalid timestamp format: {timestamp}")


# ==================== METRICS ENDPOINT TESTS ====================


class TestMetricsEndpoint:
    """Test suite for the Prometheus metrics endpoint (GET /metrics)"""

    def test_metrics_endpoint_exposed(self):
        """Test that /metrics endpoint is available and returns text metrics"""
        response = client.get("/metrics")
        assert response.status_code == 200
        assert "text/plain" in response.headers.get("content-type", "")

        metrics_text = response.text
        assert "http_requests_total" in metrics_text
        assert "http_request_duration_seconds" in metrics_text
        assert "http_requests_in_progress" in metrics_text

    def test_metrics_contain_required_labels(self):
        """Test that HTTP metrics include method, endpoint, status_code labels"""
        client.get("/")
        client.get("/health")

        response = client.get("/metrics")
        metrics_text = response.text

        assert 'method="GET"' in metrics_text
        assert 'endpoint="/"' in metrics_text
        assert 'endpoint="/health"' in metrics_text
        assert 'status_code="200"' in metrics_text

    def test_application_specific_metrics_present(self):
        """Test that application-specific business metrics are exported"""
        client.get("/")
        response = client.get("/metrics")
        metrics_text = response.text

        assert "devops_info_endpoint_calls_total" in metrics_text
        assert "devops_info_system_collection_seconds" in metrics_text


# ==================== CONFIGURATION TESTS ====================


class TestConfiguration:
    """Test environment configuration handling"""

    @patch.dict(os.environ, {"PORT": "8000"})
    def test_port_configuration(self):
        """Test that PORT environment variable is parsed correctly"""
        import importlib
        import app
        from prometheus_client import REGISTRY
        
        # Очищаем регистр метрик перед перезагрузкой
        collectors = list(REGISTRY._collector_to_names.keys())
        for collector in collectors:
            REGISTRY.unregister(collector)
        
        importlib.reload(app)
        
        assert hasattr(app, "PORT")
        assert app.PORT == 8000
