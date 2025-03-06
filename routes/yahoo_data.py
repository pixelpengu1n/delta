from fastapi import APIRouter, Query
import yfinance as yf
import pandas as pd
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

router = APIRouter()

@router.get("/data/")
def get_data(
    ticker: str = Query(..., description="The stock ticker symbol."),
    start_date: str = Query(..., description="The start date for the data (format: YYYY-MM-DD)."),
    end_date: str = Query(..., description="The end date for the data (format: YYYY-MM-DD)."),
    interval: str = Query(..., description="The time interval for the data (e.g., '1m', '5d', '1wk').")
):
    # Download the data from Yahoo Finance
    data = yf.download(ticker, start=start_date, end=end_date, interval=interval)
    
    # Valid intervals: [1m, 2m, 5m, 15m, 30m, 60m, 90m, 1h, 1d, 5d, 1wk, 1mo, 3mo]

    # Extract the 'Close' column and reset the index
    data = data[['Close']].reset_index()

    # Rename the columns
    data.columns = ['Date', 'Closing Price']

    # Print the DataFrame in a tabular format (for debugging/logging)
    print(data.to_string(index=False))  # This will print the data as a table without the index

    # Convert the DataFrame to a dictionary (list of dicts) to make it JSON serializable
    data_dict = data.to_dict(orient='records')

    # Return the data as a JSON response
    return JSONResponse(content=jsonable_encoder(data_dict))
