from fastapi import APIRouter
from fastapi.responses import Response
import yfinance as yf
import pandas as pd
import io
import matplotlib
matplotlib.use("Agg")  # Add this before importing pyplot
import matplotlib.pyplot as plt

def fetch_crypto_data(ticker: str, start_date: str, end_date: str, interval: str):
    data = yf.download(ticker, start=start_date, end=end_date, interval=interval)
    data = data[['Close', 'Volume']].reset_index()
    data.columns = ['Date', 'Closing Price', 'Volume']
    return data

def generate_price_chart(data: pd.DataFrame, ticker: str):
    plt.figure(figsize=(12, 6))  # Increase figure size (width=12, height=6)
    plt.plot(data['Date'], data['Closing Price'], marker='o', linestyle='-')
    
    plt.xlabel("Date", fontsize=12)  
    plt.ylabel("Closing Price (USD)", fontsize=12)  
    plt.title(f"{ticker} Price Trend", fontsize=14)  
    plt.xticks(rotation=45, fontsize=10)  
    plt.yticks(fontsize=10)

    plt.tight_layout()  # Ensures nothing gets cut off

    buf = io.BytesIO()
    plt.savefig(buf, format="png", bbox_inches="tight")  # Ensures full image is saved
    buf.seek(0)

    return Response(content=buf.getvalue(), media_type="image/png")

router = APIRouter()

@router.get("/events/price_chart/")
def price_chart(ticker: str, start_date: str, end_date: str, interval: str):
    data = fetch_crypto_data(ticker, start_date, end_date, interval)
    return generate_price_chart(data, ticker)
