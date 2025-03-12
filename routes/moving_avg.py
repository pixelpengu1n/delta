from fastapi import APIRouter
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
import yfinance as yf
import pandas as pd
 
def fetch_crypto_data(ticker: str, start_date: str, end_date: str, interval: str):
    data = yf.download(ticker, start=start_date, end=end_date, interval=interval)
    data = data[['Closing Price', 'Volume']].reset_index()
    data.columns = ['Date', 'Closing Price', 'Volume']
    return data
 
def calculate_moving_averages(data: pd.DataFrame, window: int, method: str):
    if method.upper() == "EMA":
        data[f"EMA_{window}"] = data["Closing Price"].ewm(span=window, adjust=False).mean()
    else:
        data[f"SMA_{window}"] = data["Closing Price"].rolling(window=window).mean()
    return data
 
router = APIRouter()
 
@router.get("/events/moving_avg/")
def moving_average(ticker: str, start_date: str, end_date: str, interval: str, window: int = 14, method: str = "EMA"):
    data = fetch_crypto_data(ticker, start_date, end_date, interval)
    ma_data = calculate_moving_averages(data, window, method)
    return JSONResponse(content=jsonable_encoder(ma_data.to_dict(orient='records')))
