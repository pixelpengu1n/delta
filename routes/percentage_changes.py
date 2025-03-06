from fastapi import APIRouter, Query
import yfinance as yf
import pandas as pd
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

router = APIRouter()

"""
Large Percentage Changes: Where the price moves by more than a certain threshold within a single day or over a period of days.
- Threshold: We use a threshold value (default 5%) to define what counts as a "big event." If the percentage change on a given day is above this threshold, we consider it a significant event.
- Percentage Change Calculation: We calculate the percentage change in the closing price from one day to the next.
- Filtering Big Events: We filter out the dates where the percentage change in price exceeds the threshold (either a gain or a loss).
- Returning the Result: The API returns the filtered list of dates with the corresponding closing price and percentage change.
"""

@router.get("/event/percentage_change/")
def analyze_big_events(
    ticker: str = Query(..., description="The stock ticker symbol."),
    start_date: str = Query(..., description="The start date for the data (format: YYYY-MM-DD)."),
    end_date: str = Query(..., description="The end date for the data (format: YYYY-MM-DD)."),
    interval: str = Query(..., description="The time interval for the data (e.g., '1m', '5d', '1wk')."),
    threshold: float = Query(5.0, description="The percentage change threshold to identify big events (default is 5%).")
):
    # Download the data from Yahoo Finance
    data = yf.download(ticker, start=start_date, end=end_date, interval=interval)
    
    # Extract the 'Close' column and reset the index
    data = data[['Close']].reset_index()

    # Rename the columns
    data.columns = ['Date', 'Closing Price']

    # Calculate the percentage change between consecutive days
    data['Pct Change'] = data['Closing Price'].pct_change() * 100

    # Filter for big events (percentage changes that exceed the threshold)
    big_events = data[abs(data['Pct Change']) >= threshold]

    # Return the filtered data with big events
    return big_events[['Date', 'Closing Price', 'Pct Change']].to_dict(orient='records')