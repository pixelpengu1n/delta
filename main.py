from fastapi import FastAPI
from routes.greet import router as greet
from routes.yahoo_data import router as fetch
from routes.percentage_changes import router as percentage_change
import yfinance as yf
import pandas as ps

app = FastAPI()

app.include_router(greet)
app.include_router(fetch)
app.include_router(percentage_change)

if __name__ == "__main__":
    import uvicorn  
    uvicorn.run(app, host="0.0.0.0", port=8000)
