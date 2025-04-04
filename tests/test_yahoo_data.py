from unittest.mock import patch

import pandas as pd
from fastapi.testclient import TestClient

from src.lambda_function import app

client = TestClient(app)


@patch("src.routes.yahoo_data.yf.download")
def test_retrieve_stock_data(mock_yfinance):
    # Setup realistic mock data
    mock_data = pd.DataFrame(
        {
            "Date": ["2024-01-01"],
            "Open": [100],
            "High": [101],
            "Low": [99],
            "Close": [100.5],
            "Volume": [1000000],
        }
    )

    mock_data["Date"] = pd.to_datetime(mock_data["Date"])
    mock_data.set_index("Date", inplace=True)

    mock_yfinance.return_value = mock_data

    response = client.get(
        "/api/retrieve",
        params={
            "ticker": "AAPL",
            "start_date": "2024-01-01",
            "end_date": "2024-01-10",
            "interval": "1d",
        },
    )

    assert response.status_code == 200
    data = response.json()
    assert data["data_source"] == "Yahoo Finance"
    assert len(data["events"]) == 1
    assert data["events"][0]["attribute"]["ticker"] == "AAPL"


@patch("src.routes.yahoo_data.yf.download")
def test_retrieve_invalid_params(mock_yfinance):
    # Simulate empty DataFrame to trigger 404
    mock_yfinance.return_value = pd.DataFrame()

    response = client.get(
        "/api/retrieve",
        params={
            "ticker": "",
            "start_date": "invalid-date",
            "end_date": "2024-01-10",
            "interval": "1d",
        },
    )

    # Should either be 404 (custom handling) or 422 (validation error)
    assert response.status_code in [404, 422]
