import pytest
from fastapi.testclient import TestClient
from main import app
import json

client = TestClient(app)

def test_retrieve_stock_data():
    params = {
        "ticker": "AAPL",
        "start_date": "2024-01-01",
        "end_date": "2024-01-10",
        "interval": "1d"
    }

    response = client.get("/retrieve/", params=params)

    assert response.status_code == 200
    json_response = response.json()

    assert json_response["data_source"] == "Yahoo Finance"
    assert json_response["dataset_type"] == "Stock Market Data"
    assert "events" in json_response
    assert len(json_response["events"]) > 0

    event = json_response["events"][0]
    assert "time_object" in event
    assert "attribute" in event
    assert event["attribute"]["ticker"] == "AAPL"

def test_retrieve_no_data():
    params = {
        "ticker": "INVALIDTICKER",
        "start_date": "2024-01-01",
        "end_date": "2024-01-02",
        "interval": "1d"
    }

    response = client.get("/retrieve/", params=params)

    assert response.status_code == 404
    json_response = response.json()

    assert json_response["error"] == "No data found for the given parameters."