from fastapi.testclient import TestClient
from unittest.mock import patch
import pandas as pd
from main import app  
 
client = TestClient(app)
 
# Sample mock data for BTC-USD prices
mock_data = pd.DataFrame({
    "Date": ["2024-01-01", "2024-01-02", "2024-01-03"],
    "Close": [43000, 43200, 43500],
    "Volume": [1200, 1300, 1100]
})
 
mock_data = mock_data.rename(columns={"Close": "Closing Price"})
 
@patch("yfinance.download")
def test_moving_average(mock_yf_download):
    mock_yf_download.return_value = mock_data
 
    response = client.get(
        "/events/moving_avg/",
        params={
            "ticker": "BTC-USD",
            "start_date": "2024-01-01",
            "end_date": "2024-01-05",
            "interval": "1d",
            "window": 3,
            "method": "EMA"
        }
    )
 
    assert response.status_code == 200
    json_data = response.json()
 
    # Ensure the response contains the moving average column
    assert all("EMA_3" in entry for entry in json_data)
    assert len(json_data) == 3  # Should have same length as input data
