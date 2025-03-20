from fastapi import APIRouter, Query
import yfinance as yf
import pandas as pd
from datetime import datetime, timezone
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

router = APIRouter()

@router.get("/retrieve/")
def get_data(
    ticker: str = Query(..., description="The stock ticker symbol."),
    start_date: str = Query(..., description="The start date for the data (format: YYYY-MM-DD)."),
    end_date: str = Query(..., description="The end date for the data (format: YYYY-MM-DD)."),
    interval: str = Query(..., description="The time interval for the data (e.g., '1m', '5d', '1wk').")
):
    # Download the data from Yahoo Finance
    data = yf.download(ticker, start=start_date, end=end_date, interval=interval)
    
    if data.empty:
        return JSONResponse(content={"error": "No data found for the given parameters."}, status_code=404)
    
    # Convert index to a datetime column
    data.reset_index(inplace=True)
    
    # Ensure the timestamp is properly formatted as an ISO string
    data["Date"] = pd.to_datetime(data["Date"], errors='coerce').dt.strftime('%Y-%m-%dT%H:%M:%SZ')
    
    # Convert data to follow the ADAGE3 event data model
    json_response = {
        "data_source": "Yahoo Finance",
        "dataset_type": "Stock Market Data",
        "dataset_id": f"https://finance.yahoo.com/quote/{ticker}",
        "time_object": {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "timezone": "UTC"
        },
        "events": []
    }
    
    for _, row in data.iterrows():
        # Ensure all attributes are properly formatted as single values
        attributes = {
            "ticker": ticker,
            "open": row.get("Open", None),
            "high": row.get("High", None),
            "low": row.get("Low", None),
            "close": row.get("Close", None),
            "volume": row.get("Volume", None)
        }

        # If attributes contain a nested dictionary with an empty string as a key, extract the value
        for key, value in attributes.items():
            if isinstance(value, dict) and "" in value:
                attributes[key] = value[""]

        event = {
            "time_object": {
                "timestamp": {"": row["Date"]},  # Ensure the timestamp follows the expected format
                "duration": 1,
                "duration_unit": interval,
                "timezone": "UTC"
            },
            "event_type": "stock price update",
            "attribute": attributes
        }
        json_response["events"].append(event)
    
    return JSONResponse(content=jsonable_encoder(json_response))
