from fastapi.testclient import TestClient
from main import app  

client = TestClient(app)

def test_download_csv():
    response = client.get(
        "/data/csv/",
        params={
            "ticker": "BTC-USD",
            "start_date": "2024-01-01",
            "end_date": "2024-01-10",
            "interval": "1d"
        }
    )
    
    assert response.status_code == 200
    assert "text/csv" in response.headers["content-type"]  # Fix: Check if "text/csv" is present
    assert "Content-Disposition" in response.headers
    assert "attachment; filename=BTC-USD_data.csv" in response.headers["Content-Disposition"]

    csv_data = response.text.strip()
    assert "Date,Closing Price,Volume" in csv_data  # Checking if the header exists
