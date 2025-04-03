import pytest
from fastapi.testclient import TestClient
from main import app  # Replace with your actual FastAPI app file if it's not named main.py
import io
import warnings

client = TestClient(app)


def test_collect_valid_csv():
    """Test collecting valid CSV event data."""
    csv_content = "timestamp,event_type,value\n2024-01-01T00:00:00Z,login,100\n2024-01-02T00:00:00Z,logout,200"
    file = {"file": ("valid.csv", io.BytesIO(csv_content.encode("utf-8")), "text/csv")}

    response = client.post("/collect/", files=file, params={
        "data_source": "test_source",
        "dataset_type": "user_activity",
        "timestamp_column": "timestamp",
        "event_type_column": "event_type",
        "duration": 10,
        "duration_unit": "minute",
        "timezone": "UTC"
    })

    assert response.status_code == 200
    json_response = response.json()

    assert json_response["data_source"] == "test_source"
    assert json_response["dataset_type"] == "user_activity"
    assert "dataset_id" in json_response
    assert len(json_response["events"]) == 2

    first_event = json_response["events"][0]
    assert first_event["event_type"] == "login"
    assert first_event["time_object"]["duration"] == 10
    assert first_event["attribute"]["value"] == 100  # Should remain int or str, depending on CSV parser

def test_collect_csv_missing_timestamp_column():
    """Test behavior when timestamp column is missing in the CSV."""
    csv_content = "event_type,value\nlogin,100"
    file = {"file": ("missing_timestamp.csv", io.BytesIO(csv_content.encode("utf-8")), "text/csv")}

    response = client.post("/collect/", files=file)

    assert response.status_code == 200
    assert len(response.json()["events"]) == 0  # No timestamp = no valid events

def test_collect_csv_without_event_type_column():
    """Test when event_type_column is not passed explicitly."""
    csv_content = "timestamp,value\n2024-01-01T00:00:00Z,100"
    file = {"file": ("no_event_type.csv", io.BytesIO(csv_content.encode("utf-8")), "text/csv")}

    response = client.post("/collect/", files=file, params={
        "timestamp_column": "timestamp"
    })

    assert response.status_code == 200
    assert response.json()["events"][0]["event_type"] == "generic_event"

def test_collect_empty_csv():
    """Test uploading an empty CSV."""
    file = {"file": ("empty.csv", io.BytesIO(b""), "text/csv")}

    response = client.post("/collect/", files=file)

    assert response.status_code == 400
    assert "CSV file is empty" in response.json()["detail"]

def test_collect_malformed_csv():
    """Test uploading a malformed CSV."""
    malformed_csv = "timestamp,event_type,value\n2024-01-01T00:00:00Z,login\nbad_line_without_enough_columns"
    file = {"file": ("bad.csv", io.BytesIO(malformed_csv.encode("utf-8")), "text/csv")}

    response = client.post("/collect/", files=file)

    # Depending on pandas' tolerance, might still succeed but skip malformed rows
    assert response.status_code in [200, 500]
    if response.status_code == 200:
        assert isinstance(response.json()["events"], list)
