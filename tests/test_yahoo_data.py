from fastapi.testclient import TestClient
from main import app  

client = TestClient(app)

def test_get_data():
    response = client.get(
        "/data/",
        params={
            "ticker": "AAPL",
            "start_date": "2024-01-01",
            "end_date": "2024-01-10",
            "interval": "1d"
        }
    )
    assert response.status_code == 200
    json_data = response.json()
    assert isinstance(json_data, list)  # Ensure response is a list of dictionaries
    if json_data:  # Only check structure if data exists
        assert "Date" in json_data[0]
        assert "Closing Price" in json_data[0]
