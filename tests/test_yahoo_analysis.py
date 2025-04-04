import json
from io import BytesIO

import pytest
from fastapi.testclient import TestClient

from src.lambda_function import app

client = TestClient(app)


@pytest.fixture
def sample_yahoo_data():
    return {
        "cleaned_data": [
            {
                "dataset_id": "yahoo_test",
                "events": [
                    {
                        "time_object": {"timestamp": "2024-01-01T12:00:00Z"},
                        "attribute": {"ticker": "AAPL", "open": 100.0, "close": 105.0},
                    }
                ],
            }
        ]
    }


def test_analyze_yahoo_valid(sample_yahoo_data):
    response = client.post(
        "/api/analyse_yahoo",
        files={
            "file": (
                "data.json",
                BytesIO(json.dumps(sample_yahoo_data).encode("utf-8")),
                "application/json",
            )
        },
    )
    assert response.status_code == 200
    assert "AAPL" in response.json()["analysis_results"]
    assert (
        response.json()["analysis_results"]["AAPL"]["summary"]["statistics"]["open"][
            "mean"
        ]
        == 100.0
    )


def test_analyze_yahoo_empty():
    response = client.post(
        "/api/analyse_yahoo",
        files={
            "file": ("empty.json", BytesIO(b'{"cleaned_data": []}'), "application/json")
        },
    )
    assert response.status_code == 200
    assert response.json()["analysis_results"] == {}


def test_analyze_yahoo_invalid():
    response = client.post(
        "/api/analyse_yahoo",
        files={"file": ("invalid.json", BytesIO(b"{"), "application/json")},
    )
    assert response.status_code == 400
