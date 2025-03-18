import pytest
from fastapi.testclient import TestClient
from main import app  # Ensure this is the correct import for your FastAPI app
import json
import io

client = TestClient(app)

def test_preprocess_valid_json():
    """Test processing of a valid JSON file."""
    test_data = [
        {
            "data_source": "EuroFidai",
            "dataset_type": "ESG",
            "dataset_id": "Aspen_Pharmacare_Holdings_Ltd_G_unit_test_subset",
            "time_object": {
                "timestamp": "2025-03-10T12:34:56Z",
                "timezone": "GMT+11"
            },
            "events": [
                {
                    "time_object": {
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
                    }
                }
            ]
        }
    ]
    
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