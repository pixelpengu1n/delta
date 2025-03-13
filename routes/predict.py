from fastapi import APIRouter, Query
import yfinance as yf
import pandas as pd
from prophet import Prophet
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

router = APIRouter()

def fetch_yahoo_data(symbol: str, start_date: str, end_date: str, interval: str = "1d"):
    """Fetches historical crypto/stock price data using Yahoo Finance."""
    data = yf.download(symbol, start=start_date, end=end_date, interval=interval)
    if data.empty:
        return None
    data = data[['Close']].reset_index()
    data.columns = ['ds', 'y']  # Prophet requires columns to be named 'ds' and 'y'
    return data

def predict_future_prices(data: pd.DataFrame, days_ahead: int):
    """Trains a Prophet model on Yahoo Finance data and predicts future prices."""
    model = Prophet()
    model.fit(data)
    
    future = model.make_future_dataframe(periods=days_ahead)
    forecast = model.predict(future)
    
    return forecast.tail(days_ahead)[["ds", "yhat", "yhat_lower", "yhat_upper"]]

@router.get("/predict/")
def predict(
    symbol: str = Query("BTC-USD", description="Crypto or stock ticker (e.g., BTC-USD, ETH-USD, AAPL)"),
    start_date: str = Query("2023-01-01", description="Start date for historical data (YYYY-MM-DD)"),
    end_date: str = Query("2024-01-01", description="End date for historical data (YYYY-MM-DD)"),
    days_ahead: int = Query(7, description="Number of days to predict")
):
    """Fetches Yahoo Finance data and predicts future prices using Prophet."""
    df = fetch_yahoo_data(symbol, start_date, end_date)

    if df is None:
        return JSONResponse(status_code=400, content={"error": "Failed to fetch data from Yahoo Finance"})

    forecast = predict_future_prices(df, days_ahead)
    
    return JSONResponse(content=jsonable_encoder(forecast.to_dict(orient="records")))
