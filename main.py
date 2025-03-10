from fastapi import FastAPI
from routes.greet import router as greet
from routes.yahoo_data import router as fetch
from routes.percentage_changes import router as percentage_change
from routes.price_chart import router as price_chart

app = FastAPI()

app.include_router(greet)
app.include_router(fetch)
app.include_router(percentage_change)
app.include_router(price_chart)

@app.get("/")
def read_root():
    return {"message": "Welcome to Delta Finances API!"}

if __name__ == "__main__":
    import uvicorn  
    uvicorn.run(app, host="0.0.0.0", port=8000)