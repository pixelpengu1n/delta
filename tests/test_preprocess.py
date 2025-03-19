import pytest
from fastapi.testclient import TestClient
from main import app  # Ensure this matches your FastAPI app import
import json
import io
import numpy as np

client = TestClient(app)

def test_preprocess_valid_json():
    """Test processing of a valid JSON file."""
    test_data = [
        {
            "data_source": "Yahoo Finance",
            "dataset_type": "Stock Market Data",
            "dataset_id": "BTC-USD",
            "time_object": {
                "timestamp": "2025-03-18T05:36:43.410523+00:00",
                "timezone": "UTC"
            },
            "events": [
                {
                    "time_object": {
                        "timestamp": "2024-01-01T00:00:00Z",
                        "timezone": "UTC"
                    },
                    "event_type": "stock price update",
                    "attribute": {
                        "ticker": "BTC-USD",
                        "open": "43000",
                        "high": "44000",
                        "low": "42000",
                        "close": "43500",
                        "volume": "1500"
                    }
                }
            ]
        }
    ]

    json_bytes = json.dumps(test_data).encode("utf-8")
    file = {"file": ("test.json", io.BytesIO(json_bytes), "application/json")}

    response = client.post("/preprocess/", files=file)

    assert response.status_code == 200
    json_response = response.json()
    
    assert "cleaned_data" in json_response
    assert len(json_response["cleaned_data"]) == 1  # Ensure dataset is retained
    assert len(json_response["cleaned_data"][0]["events"]) == 1  # Ensure events are processed
    
    # Validate data type conversions
    processed_event = json_response["cleaned_data"][0]["events"][0]
    assert isinstance(processed_event["attribute"]["open"], float)  # Converted to float
    assert isinstance(processed_event["attribute"]["close"], float)  # Converted to float

def test_preprocess_invalid_json():
    """Test processing of an invalid JSON file."""
    invalid_json = "{"  # Broken JSON format
    file = {"file": ("invalid.json", io.BytesIO(invalid_json.encode("utf-8")), "application/json")}

    response = client.post("/preprocess/", files=file)

    assert response.status_code == 400  # Should return 400 now

def test_preprocess_empty_json():
    """Test processing of an empty JSON file."""
    empty_json = []
    file = {"file": ("empty.json", io.BytesIO(json.dumps(empty_json).encode("utf-8")), "application/json")}

    response = client.post("/preprocess/", files=file)

    assert response.status_code == 200
    json_response = response.json()

    assert "cleaned_data" in json_response
    assert json_response["cleaned_data"] == []  # Now correctly returns an empty list

def test_preprocess_nan_handling():
    """Ensure NaN values are properly replaced with None."""
    test_data = [
        {
            "data_source": "Finance API",
            "dataset_type": "Stock Data",
            "dataset_id": "BTC-USD",
            "events": [
                {
                    "event_type": "price_update",
                    "attribute": {
                        "price": float("NaN"),
                        "volume": 1000
                    }
                }
            ]
        }
    ]

    json_bytes = json.dumps(test_data, default=lambda x: None if isinstance(x, float) and np.isnan(x) else x).encode("utf-8")
    file = {"file": ("nan_test.json", io.BytesIO(json_bytes), "application/json")}

    response = client.post("/preprocess/", files=file)

    assert response.status_code == 200
    json_response = response.json()

    processed_attributes = json_response["cleaned_data"][0]["events"][0]["attribute"]
    assert processed_attributes["price"] is None  # NaN should be converted to None
