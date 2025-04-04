import json
from io import BytesIO

from fastapi.testclient import TestClient

from src.lambda_function import app

client = TestClient(app)


def test_analyze_data():
    test_data = {
        "cleaned_data": [
            {
                "dataset_id": "123",
                "dataset_type": "type_test",
                "events": [
                    {
                        "event_type": "event1",
                        "time_object": {"timestamp": "2024-01-01T12:00:00Z"},
                        "attribute": {"value": 100},
                    },
                    {
                        "event_type": "event2",
                        "time_object": {"timestamp": "2024-01-02T12:00:00Z"},
                        "attribute": {"value": 200},
                    },
                ],
            }
        ]
    }

    json_bytes = json.dumps(test_data).encode("utf-8")
    response = client.post(
        "/api/analyse",
        files={"file": ("test.json", BytesIO(json_bytes), "application/json")},
    )

    assert response.status_code == 200
    assert response.json()["status"] == "success"
