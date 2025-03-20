import pytest
from fastapi.testclient import TestClient
from main import app  # Ensure this matches your FastAPI app import
import json
import io
import numpy as np

client = TestClient(app)

def test_analyze_yahoo_valid_json():
    """Test analysis of a valid Yahoo Finance JSON file."""
    test_data = {
        "cleaned_data": [
            {
                "events": [
                    {
                        "time_object": {"timestamp": "2025-03-20T12:00:00Z"},
                        "attribute": {
                            "ticker": "AAPL",
                            "open": 150.0,
                            "high": 155.0,
                            "low": 149.5,
                            "close": 153.0,
                            "volume": 50000
                        }
                    },
                    {
                        "time_object": {"timestamp": "2025-03-21T12:00:00Z"},
                        "attribute": {
                            "ticker": "AAPL",
                            "open": 152.0,
                            "high": 157.0,
                            "low": 151.0,
                            "close": 156.0,
                            "volume": 52000
                        }
                    }
                ]
            }
        ]
    }
    
    json_bytes = json.dumps(test_data).encode("utf-8")
    file = {"file": ("test.json", io.BytesIO(json_bytes), "application/json")}

    response = client.post("/analyse_yahoo/", files=file)

    assert response.status_code == 200
    json_response = response.json()
    
    assert "analysis_results" in json_response
    assert "AAPL" in json_response["analysis_results"]
    
    summary = json_response["analysis_results"]["AAPL"]["summary"]
    assert "statistics" in summary
    assert "open" in summary["statistics"]
    assert "mean" in summary["statistics"]["open"]

def test_analyze_yahoo_empty_json():
    """Test analysis of an empty JSON file."""
    empty_json = {"cleaned_data": []}
    file = {"file": ("empty.json", io.BytesIO(json.dumps(empty_json).encode("utf-8")), "application/json")}

    response = client.post("/analyse_yahoo/", files=file)

    assert response.status_code == 200
    json_response = response.json()

    assert "analysis_results" in json_response
    assert json_response["analysis_results"] == {}  # Should return an empty analysis

def test_analyze_yahoo_invalid_json():
    """Test analysis of an invalid JSON file."""
    invalid_json = "{"  # Broken JSON format
    file = {"file": ("invalid.json", io.BytesIO(invalid_json.encode("utf-8")), "application/json")}

    response = client.post("/analyse_yahoo/", files=file)

    assert response.status_code == 400  # Should return a 400 error
