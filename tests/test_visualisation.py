# import pytest
# from fastapi.testclient import TestClient
# from main import app  # Ensure this is your FastAPI main file
# import json
# import io

# client = TestClient(app)

# def test_visualisation_valid_json():
#     """Test valid JSON input for visualisation API."""
#     test_data = {
#         "cleaned_data": [
#             {
#                 "data_source": "Yahoo Finance",
#                 "dataset_type": "Stock Market Data",
#                 "dataset_id": "BTC-AUD",
#                 "time_object": {"timestamp": "2025-03-18T05:36:43.410523+00:00", "timezone": "UTC"},
#                 "events": [
#                     {
#                         "time_object": {"timestamp": "2024-01-01T00:00:00Z"},
#                         "event_type": "stock price update",
#                         "attribute": {
#                             "ticker": "BTC-AUD",
#                             "open": 43000,
#                             "high": 44000,
#                             "low": 42000,
#                             "close": 43500,
#                             "volume": 1500
#                         }
#                     }
#                 ]
#             }
#         ]
#     }

#     json_bytes = json.dumps(test_data).encode("utf-8")
#     file = {"file": ("test.json", io.BytesIO(json_bytes), "application/json")}

#     response = client.post("/visualise/", files=file)

#     assert response.status_code == 200
#     assert response.headers["content-type"] == "image/png"

# def test_visualisation_empty_json():
#     """Test empty JSON input handling."""
#     empty_json = {"cleaned_data": []}
#     file = {"file": ("empty.json", io.BytesIO(json.dumps(empty_json).encode("utf-8")), "application/json")}

#     response = client.post("/visualise/", files=file)

#     assert response.status_code == 400
#     assert "No suitable visualisation available." in response.json()["detail"]

# def test_visualisation_invalid_json():
#     """Test invalid JSON input handling."""
#     invalid_json = "{"  # Broken JSON
#     file = {"file": ("invalid.json", io.BytesIO(invalid_json.encode("utf-8")), "application/json")}

#     response = client.post("/visualise/", files=file)

#     assert response.status_code == 400
#     assert "Visualisation error" in response.json()["detail"]

# def test_visualisation_no_file():
#     """Test API response when no file is sent."""
#     response = client.post("/visualise/")

#     assert response.status_code == 422  # FastAPI expects a file, so it should return 422
