from fastapi.testclient import TestClient
from main import app  

client = TestClient(app)

def test_whale_activity():
    response = client.get(
        "/events/whale_activity/",
        params={
            "ticker": "BTC-USD",
            "start_date": "2024-01-01",
            "end_date": "2024-01-10",
            "interval": "1d",
            "volume_threshold": 2.0
        }
    )
    assert response.status_code == 200
    json_data = response.json()
    assert isinstance(json_data, list)  # Ensure response is a list

    if json_data:  # If there is whale activity, check structure
        assert "Date" in json_data[0]
        assert "Closing Price" in json_data[0]
        assert "Volume" in json_data[0]
        assert isinstance(json_data[0]["Volume"], (int, float))  # Ensure volume is numeric
