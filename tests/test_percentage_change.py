from fastapi.testclient import TestClient
from main import app  

client = TestClient(app)

def test_analyze_big_events():
    response = client.get(
        "/event/percentage_change/",
        params={
            "ticker": "AAPL",
            "start_date": "2024-01-01",
            "end_date": "2024-01-10",
            "interval": "1d",
            "threshold": 5.0
        }
    )
    assert response.status_code == 200
    json_data = response.json()
    assert isinstance(json_data, list)  # Ensure response is a list of dictionaries

    if json_data:  # Only check structure if data exists
        assert "Date" in json_data[0]
        assert "Closing Price" in json_data[0]
        assert "Pct Change" in json_data[0]
        assert isinstance(json_data[0]["Pct Change"], float)  # Ensure percentage change is a float
