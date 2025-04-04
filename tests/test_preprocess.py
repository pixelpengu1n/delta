import json
from io import BytesIO

import numpy as np
from fastapi.testclient import TestClient

from src.lambda_function import app

client = TestClient(app)


def test_preprocess_valid_json():
    test_data = {
        "dataset_id": "test123",
        "events": [
            {
                "time_object": {"timestamp": "2024-01-01"},
                "attribute": {"value": 100, "nan_value": np.nan},
            }
        ],
    }

    response = client.post(
        "/api/preprocess",
        files={
            "file": (
                "data.json",
                BytesIO(
                    json.dumps(
                        test_data,
                        default=lambda x: (
                            None if isinstance(x, float) and np.isnan(x) else x
                        ),
                    ).encode("utf-8")
                ),
                "application/json",
            )
        },
    )
    assert response.status_code == 200


def test_preprocess_invalid_json():
    response = client.post(
        "/api/preprocess",
        files={"file": ("bad.json", BytesIO(b"{"), "application/json")},
    )
    assert response.status_code == 400
