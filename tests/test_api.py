"""
Tests for the House Pricing API. These tests cover basic functionality, valid input cases, and invalid input cases to ensure the API behaves as expected under different scenarios.
Ejecutar con: pytest tests/test_api.py -v
"""
import pytest
import numpy as np
from unittest.mock import patch, MagicMock
from fastapi.testclient import TestClient
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# Mock the model loading so tests don't require .pkl files to be present
mock_model = MagicMock()
mock_model.predict.return_value = np.array([200000.0])

mock_pipeline = MagicMock()
mock_pipeline.transform.return_value = np.zeros((1, 10))

with patch("app.model.joblib.load", side_effect=[mock_model, mock_pipeline]):
    with patch("app.model.model", mock_model):
        with patch("app.model.preprocess_pipeline", mock_pipeline):
            from app.main import app

client = TestClient(app)


# ============================================================================
# BASIC TESTS (3 tests)
# ============================================================================

def test_health():
    """API is healthy and returns correct status"""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "OK"


def test_docs_disponible():
    """Doc is available at /docs"""
    response = client.get("/docs")
    assert response.status_code == 200


@patch("app.model.predict_price", return_value=np.array([200000.0]))
def test_prediccion_basica(mock_predict):
    """Prediction endpoint returns a valid response for basic input"""
    payload = {
        "OverallQual": 7,
        "GrLivArea": 1500,
        "GarageCars": 2,
        "GarageArea": 480,
        "TotalBsmtSF": 900
    }
    response = client.post("/v1/predict", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "predicted_price" in data
    assert data["predicted_price"] > 0


# ============================================================================
# VALID INPUT CASES TESTS (3 tests)
# ============================================================================

@patch("app.model.predict_price", return_value=np.array([120000.0]))
def test_1(mock_predict):
    payload = {
        "OverallQual": 3,
        "GrLivArea": 800,
        "GarageCars": 1,
        "GarageArea": 200,
        "TotalBsmtSF": 400
    }
    response = client.post("/v1/predict", json=payload)
    assert response.status_code == 200
    assert response.json()["predicted_price"] > 0


@patch("app.model.predict_price", return_value=np.array([450000.0]))
def test_2(mock_predict):
    payload = {
        "OverallQual": 9,
        "GrLivArea": 3000,
        "GarageCars": 3,
        "GarageArea": 800,
        "TotalBsmtSF": 1500
    }
    response = client.post("/v1/predict", json=payload)
    assert response.status_code == 200
    assert response.json()["predicted_price"] > 0


@patch("app.model.predict_price", return_value=np.array([175000.0]))
def test_3(mock_predict):
    payload = {
        "OverallQual": 6,
        "GrLivArea": 1200,
        "GarageCars": 0,
        "GarageArea": 0,
        "TotalBsmtSF": 600
    }
    response = client.post("/v1/predict", json=payload)
    assert response.status_code == 200


# ============================================================================
# NON VALID INPUT CASES (4 tests)
# ============================================================================

def test_quality_range():
    """OverallQual out of range (1-10)"""
    payload = {
        "OverallQual": 11,
        "GrLivArea": 1500,
        "GarageCars": 2,
        "GarageArea": 480,
        "TotalBsmtSF": 900
    }
    response = client.post("/v1/predict", json=payload)
    assert response.status_code == 422


def test_area_negative():
    """Negative values for area features should be invalid"""
    payload = {
        "OverallQual": 7,
        "GrLivArea": -100,
        "GarageCars": 2,
        "GarageArea": 480,
        "TotalBsmtSF": 900
    }
    response = client.post("/v1/predict", json=payload)
    assert response.status_code == 422


def test_missing_fields():
    """All fields are required, missing any should cause validation error"""
    payload = {
        "OverallQual": 7,
        "GrLivArea": 1500,
    }
    response = client.post("/v1/predict", json=payload)
    assert response.status_code == 422


def test_datatype():
    """Data type mismatch (string instead of int) should cause validation error"""
    payload = {
        "OverallQual": "seven",
        "GrLivArea": 1500,
        "GarageCars": 2,
        "GarageArea": 480,
        "TotalBsmtSF": 900
    }
    response = client.post("/v1/predict", json=payload)
    assert response.status_code == 422


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
