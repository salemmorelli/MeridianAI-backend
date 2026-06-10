# tests/test_main.py
from __future__ import annotations
import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

class TestHealthEndpoint:
    def test_health_returns_200(self):
        response = client.get("/health")
        assert response.status_code == 200

    def test_health_returns_ok_status(self):
        response = client.get("/health")
        assert response.json() == {"status": "ok"}

    def test_health_response_is_json(self):
        response = client.get("/health")
        assert "application/json" in response.headers["content-type"]

class TestPredictEndpoint:
    """Tests for the /predict endpoint."""

    def test_predict_valid_input_returns_200(self):
        """Valid prediction request should return HTTP 200."""
        response = client.post("/predict", json={
            "symptom": "headache",
            "region": "all",
            "duration_minutes": 2
        })
        assert response.status_code == 200

    def test_predict_returns_recommendation_key(self):
        """Response must contain recommendation key."""
        response = client.post("/predict", json={
            "symptom": "headache",
            "region": "all",
            "duration_minutes": 1
        })
        data = response.json()
        assert "recommendation" in data

    def test_predict_recommendation_has_point_code(self):
        """Recommendation must contain point_code."""
        response = client.post("/predict", json={
            "symptom": "headache",
            "region": "all",
            "duration_minutes": 1
        })
        data = response.json()
        assert "point_code" in data["recommendation"]

    def test_predict_recommendation_has_location(self):
        """Recommendation must contain location."""
        response = client.post("/predict", json={
            "symptom": "headache",
            "region": "all",
            "duration_minutes": 1
        })
        data = response.json()
        assert "location" in data["recommendation"]

    def test_predict_missing_symptom_returns_422(self):
        """Missing required field should return HTTP 422 Unprocessable Entity."""
        response = client.post("/predict", json={
            "region": "head",
            "duration_minutes": 2
        })
        assert response.status_code == 422

    def test_predict_duration_too_high_returns_422(self):
        """Duration above maximum (10) should return HTTP 422."""
        response = client.post("/predict", json={
            "symptom": "headache",
            "region": "head",
            "duration_minutes": 99
        })
        assert response.status_code == 422

    def test_predict_duration_too_low_returns_422(self):
        """Duration below minimum (1) should return HTTP 422."""
        response = client.post("/predict", json={
            "symptom": "headache",
            "region": "head",
            "duration_minutes": 0
        })
        assert response.status_code == 422

    def test_predict_empty_body_returns_422(self):
        """Empty request body should return HTTP 422."""
        response = client.post("/predict", json={})
        assert response.status_code == 422

    def test_predict_returns_input_echo(self):
        """Response should echo back the input."""
        payload = {
            "symptom": "headache",
            "region": "all",
            "duration_minutes": 2
        }
        response = client.post("/predict", json=payload)
        data = response.json()
        assert "input" in data
        assert data["input"]["symptom"] == "headache"


class TestFeedbackEndpoint:
    """Tests for the /feedback endpoint."""

    def test_feedback_valid_input_returns_200(self):
        """Valid feedback should return HTTP 200."""
        response = client.post("/feedback", json={
            "session_id": "test-session-001",
            "symptom": "headache",
            "region": "head",
            "selected_meridian": "gallbladder",
            "duration_minutes": 2,
            "recommended_point": "GB20",
            "helped": True
        })
        assert response.status_code == 200

    def test_feedback_returns_ok_status(self):
        """Feedback response must contain status ok."""
        response = client.post("/feedback", json={
            "session_id": "test-session-002",
            "symptom": "stress",
            "region": "hand",
            "duration_minutes": 3,
            "recommended_point": "LI4",
            "helped": False
        })
        data = response.json()
        assert data["status"] == "ok"

    def test_feedback_returns_feedback_id(self):
        """Feedback response must contain a feedback_id."""
        response = client.post("/feedback", json={
            "session_id": "test-session-003",
            "symptom": "fatigue",
            "region": "leg",
            "duration_minutes": 5,
            "recommended_point": "ST36",
            "helped": True
        })
        data = response.json()
        assert "feedback_id" in data

    def test_feedback_missing_required_field_returns_422(self):
        """Missing helped field should return HTTP 422."""
        response = client.post("/feedback", json={
            "session_id": "test-session-004",
            "symptom": "headache",
            "region": "head",
            "duration_minutes": 2,
            "recommended_point": "GB20"
            # helped is missing
        })
        assert response.status_code == 422


class TestCatalogEndpoint:
    """Tests for catalog-dependent behaviour."""

    def test_predict_point_code_is_string(self):
        """Point code in recommendation must be a string."""
        response = client.post("/predict", json={
            "symptom": "headache",
            "region": "all",
            "duration_minutes": 1
        })
        data = response.json()
        assert isinstance(data["recommendation"]["point_code"], str)

    def test_predict_technique_is_string(self):
        """Technique in recommendation must be a string."""
        response = client.post("/predict", json={
            "symptom": "headache",
            "region": "all",
            "duration_minutes": 1
        })
        data = response.json()
        assert isinstance(data["recommendation"]["technique"], str)