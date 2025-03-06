from fastapi import FastAPI
from routes.greet import router as greet
from routes.yahoo_data import router as fetch

app = FastAPI()

app.include_router(greet)
app.include_router(fetch)

if __name__ == "__main__":
    import uvicorn  
    uvicorn.run(app, host="127.0.0.1", port=8000)
