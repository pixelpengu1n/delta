from fastapi import APIRouter, Query
import yfinance as yf
import pandas as pd
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

router = APIRouter()

@router.get("/data/percen_chang/")
def analyze_big_events(
    ticker: str = Query(..., description="The stock ticker symbol."),
    start_date: str = Query(..., description="The start date for the data (format: YYYY-MM-DD)."),
    end_date: str = Query(..., description="The end date for the data (format: YYYY-MM-DD)."),
    interval: str = Query(..., description="The time interval for the data (e.g., '1m', '5d', '1wk')."),
    threshold: float = Query(5.0, description="The percentage change threshold to identify big events (default is 5%).")
):
    try:
        data = yf.download(ticker, start=start_date, end=end_date, interval=interval)
        
        if data.empty:
            return JSONResponse(status_code=404, content={"error": f"No data found for {ticker} from {start_date} to {end_date} using {interval} interval."})
        
        data = data[['Close']].reset_index()
        data.columns = ['Date', 'Closing Price']
        data['Pct Change'] = data['Closing Price'].pct_change() * 100

        big_events = data[abs(data['Pct Change']) >= threshold]

        if big_events.empty:
            return JSONResponse(status_code=200, content={"message": f"No significant events detected for {ticker} from {start_date} to {end_date} at {interval} interval."})

        return JSONResponse(status_code=200, content={
            "message": f"Significant changes detected for {ticker}!",
            "events": big_events[['Date', 'Closing Price', 'Pct Change']].to_dict(orient='records')
        })
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})
