from fastapi.testclient import TestClient
from main import app  

client = TestClient(app)

def test_price_chart():
    response = client.get(
        "/events/price_chart/",
        params={
            "ticker": "BTC-USD",
            "start_date": "2024-01-01",
            "end_date": "2024-01-10",
            "interval": "1d"
        }
    )
    assert response.status_code == 200
    assert response.headers["content-type"] == "image/png"
    assert len(response.content) > 0  # Ensure the image is not empty
