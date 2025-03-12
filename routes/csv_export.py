from fastapi import APIRouter, Query
from fastapi.responses import JSONResponse, StreamingResponse
from fastapi.encoders import jsonable_encoder
import io
import yfinance as yf
import pandas as pd

def fetch_crypto_data(ticker: str, start_date: str, end_date: str, interval: str):
    data = yf.download(ticker, start=start_date, end=end_date, interval=interval)
    data = data[['Close', 'Volume']].reset_index()
    data.columns = ['Date', 'Closing Price', 'Volume']
    return data

router = APIRouter()

@router.get("/data/csv/")
def download_csv(
    ticker: str, start_date: str, end_date: str, interval: str = "1d"
):
    data = fetch_crypto_data(ticker, start_date, end_date, interval)
    csv_buffer = io.StringIO()
    data.to_csv(csv_buffer, index=False)
    csv_buffer.seek(0)

    return StreamingResponse(csv_buffer, media_type="text/csv",
                             headers={"Content-Disposition": f"attachment; filename={ticker}_data.csv"})