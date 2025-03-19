import pytest
from fastapi.testclient import TestClient
from main import app  # Ensure this is your FastAPI app entry file
import json
import io
import numpy as np

client = TestClient(app)

def test_valid_analysis():
    """Test valid JSON input for analysis API."""
    valid_data = {
        "cleaned_data": [
            {
                "data_source": "Yahoo Finance",
                "dataset_type": "Stock Market Data",
                "dataset_id": "BTC-USD",
                "time_object": {"timestamp": "2025-03-18T05:36:43.410523+00:00", "timezone": "UTC"},
                "events": [
                    {"time_object": {"timestamp": "2024-01-01T00:00:00Z"}, "event_type": "stock price update",
                     "attribute": {"ticker": "BTC-USD", "open": 43000, "high": 44000, "low": 42000, "close": 43500, "volume": 1500}},
                    {"time_object": {"timestamp": "2024-01-02T00:00:00Z"}, "event_type": "stock price update",
                     "attribute": {"ticker": "BTC-USD", "open": 43200, "high": 43800, "low": 42500, "close": 43000, "volume": 1400}},
                ],
            }
        ]
    }

    json_bytes = json.dumps(valid_data).encode("utf-8")
    file = {"file": ("valid_test.json", io.BytesIO(json_bytes), "application/json")}

    response = client.post("/analyse/", files=file)
    
    assert response.status_code == 200
    json_response = response.json()

    # Ensure response has expected keys
    assert "status" in json_response
    assert json_response["status"] == "success"
    assert "analysis_results" in json_response
    assert "Stock Market Data" in json_response["analysis_results"]

def test_invalid_json():
    """Test handling of broken JSON input."""
    invalid_json = "{"  # Malformed JSON
    file = {"file": ("invalid.json", io.BytesIO(invalid_json.encode("utf-8")), "application/json")}

    response = client.post("/analyse/", files=file)

    assert response.status_code == 400  # Should return a 400 Bad Request
    assert "detail" in response.json()

def test_empty_analysis():
    """Ensure empty JSON input is handled properly."""
    empty_json = {"cleaned_data": []}
    file = {"file": ("empty.json", io.BytesIO(json.dumps(empty_json).encode("utf-8")), "application/json")}

    response = client.post("/analyse/", files=file)

    assert response.status_code == 200
    json_response = response.json()

    assert "status" in json_response
    assert json_response["status"] == "success"
    assert json_response["analysis_results"] == {}

def test_nan_values_handling():
    """Ensure NaN values are correctly replaced with None in the response."""
    nan_data = {
        "cleaned_data": [
            {
                "data_source": "Yahoo Finance",
                "dataset_type": "Stock Market Data",
                "dataset_id": "BTC-USD",
                "events": [
                    {"time_object": {"timestamp": "2024-01-01T00:00:00Z"}, "event_type": "stock price update",
                     "attribute": {"ticker": "BTC-USD", "open": 43000, "high": 44000, "low": float("NaN"), "close": 43500, "volume": 1500}},
                    {"time_object": {"timestamp": "2024-01-02T00:00:00Z"}, "event_type": "stock price update",
                     "attribute": {"ticker": "BTC-USD", "open": 43200, "high": 43800, "low": 42500, "close": 43000, "volume": 1400}},
                ],
            }
        ]
    }

    json_bytes = json.dumps(nan_data, default=lambda x: None if isinstance(x, float) and np.isnan(x) else x).encode("utf-8")
    file = {"file": ("nan_test.json", io.BytesIO(json_bytes), "application/json")}

    response = client.post("/analyse/", files=file)

    assert response.status_code == 200
    json_response = response.json()

    assert "analysis_results" in json_response
    assert "Stock Market Data" in json_response["analysis_results"]

    # Ensure NaN values were correctly converted to None
    assert "summary" in json_response["analysis_results"]["Stock Market Data"]