import pytest
from fastapi.testclient import TestClient
from main import app
import json
import io

client = TestClient(app)

def test_analyze_data():
    test_data = {
        "cleaned_data": [
            {
                "dataset_id": "123",
                "dataset_type": "type_test",
                "events": [
                    {"event_type": "event1", "time_object": {"timestamp": "2024-01-01T12:00:00"}, "attribute": {"value": 100}},
                    {"event_type": "event2", "time_object": {"timestamp": "2024-01-02T12:00:00"}, "attribute": {"value": 200}},
                    {"event_type": "event3", "time_object": {"timestamp": "2024-01-03T12:00:00"}, "attribute": {"value": 300}},
                    {"event_type": "event4", "time_object": {"timestamp": "2024-01-04T12:00:00"}, "attribute": {"value": 400}},
                    {"event_type": "event5", "time_object": {"timestamp": "2024-01-05T12:00:00"}, "attribute": {"value": 500}},
                    {"event_type": "event6", "time_object": {"timestamp": "2024-01-06T12:00:00"}, "attribute": {"value": 600}}
                ]
            }
        ]
    }

    json_bytes = json.dumps(test_data).encode("utf-8")
    file = {"file": ("test.json", io.BytesIO(json_bytes), "application/json")}

    response = client.post("/analyse/", files=file)

    assert response.status_code == 200
    json_response = response.json()

    assert json_response["status"] == "success"
    assert "analysis_results" in json_response
    assert "type_test" in json_response["analysis_results"]
    results = json_response["analysis_results"]["type_test"]

    assert "summary" in results
    assert "statistics" in results["summary"]
    assert results["summary"]["statistics"]["value"]["mean"] == 350

    assert "trends" in results
    assert results["trends"]["event_count"] == 6