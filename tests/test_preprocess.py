import pytest
from fastapi.testclient import TestClient
<<<<<<< HEAD
from main import app  # Ensure this is the correct import for your FastAPI app
import json
import io
=======
from main import app  # Ensure this matches your FastAPI app import
import json
import io
import numpy as np
>>>>>>> 2e29871 (Made minor changes)

client = TestClient(app)

def test_preprocess_valid_json():
    """Test processing of a valid JSON file."""
    test_data = [
        {
<<<<<<< HEAD
            "data_source": "EuroFidai",
            "dataset_type": "ESG",
            "dataset_id": "Aspen_Pharmacare_Holdings_Ltd_G_unit_test_subset",
            "time_object": {
                "timestamp": "2025-03-10T12:34:56Z",
                "timezone": "GMT+11"
=======
            "data_source": "Yahoo Finance",
            "dataset_type": "Stock Market Data",
            "dataset_id": "BTC-USD",
            "time_object": {
                "timestamp": "2025-03-18T05:36:43.410523+00:00",
                "timezone": "UTC"
>>>>>>> 2e29871 (Made minor changes)
            },
            "events": [
                {
                    "time_object": {
<<<<<<< HEAD
                        "timestamp": "2017-12-31 00:00:00",
                        "duration": 0,
                        "timezone": "GMT+0"
                    },
                    "event_type": "ANALYTICEMPLOYMENTCREATION",
                    "attribute": {
                        "company": "Aspen Pharmacare Holdings Ltd",
                        "perm_id": "4295888632",
                        "metric_unit": "% growth in number of employees over last year",
                        "metric_value": "-2.94",
                        "metric_year": "2017-12-31",
                        "metric_period": "",
                        "provider_name": "Clarity AI",
                        "pillar": "G",
                        "country": "South Africa",
                        "disclosure": "CALCULATED",
                        "num_pt_obs": "366"
=======
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
>>>>>>> 2e29871 (Made minor changes)
                    }
                }
            ]
        }
    ]
<<<<<<< HEAD
    
    json_bytes = json.dumps(test_data).encode("utf-8")
    file = {"file": ("test.json", io.BytesIO(json_bytes), "application/json")}
    response = client.post("/preprocess/", files=file)
    assert response.status_code == 200
    assert "cleaned_data" in response.json()

def test_preprocess_invalid_json():
    """Test processing of an invalid JSON file."""
    invalid_json = "{"  # Broken JSON
    file = {"file": ("invalid.json", io.BytesIO(invalid_json.encode("utf-8")), "application/json")}
    response = client.post("/preprocess/", files=file)
    assert response.status_code == 500  # Adjusted to match FastAPI's default behavior
    assert "detail" in response.json()

def test_preprocess_empty_json():
    """Test processing of an empty JSON file."""
    empty_json = "[]"
    file = {"file": ("empty.json", io.BytesIO(empty_json.encode("utf-8")), "application/json")}
    response = client.post("/preprocess/", files=file)
    assert response.status_code == 200
    assert "cleaned_data" in response.json()
    assert response.json()["cleaned_data"] == []

def test_preprocess_missing_file():
    """Test endpoint without sending a file."""
    response = client.post("/preprocess/")
    assert response.status_code == 422  # FastAPI requires the file parameter
=======

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
>>>>>>> 2e29871 (Made minor changes)
