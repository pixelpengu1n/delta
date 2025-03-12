from fastapi import APIRouter, Query
import yfinance as yf
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

router = APIRouter()

def fetch_crypto_data(ticker: str, start_date: str, end_date: str, interval: str):
    data = yf.download(ticker, start=start_date, end=end_date, interval=interval)
    data = data[['Close', 'Volume']].reset_index()
    data.columns = ['Date', 'Closing Price', 'Volume']
    return data

# Endpoint for detecting whale activity (large volume spikes)
@router.get("/events/whale_activity/")
def whale_activity(
    ticker: str, start_date: str, end_date: str, interval: str, volume_threshold: float = 2.0
):
    data = fetch_crypto_data(ticker, start_date, end_date, interval)

    avg_volume = data['Volume'].mean()
    whales = data[data['Volume'] > (avg_volume * volume_threshold)]

    return JSONResponse(content=jsonable_encoder(whales.to_dict(orient='records')))
