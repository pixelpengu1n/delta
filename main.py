from fastapi import FastAPI
from routes.greet import router as greet
from routes.yahoo_data import router as retrieve
from routes.preprocess import router as preprocess
from routes.analytics import router as analytics
# from routes.visualisation import router as visualise
from routes.yahoo_analyse import router as yahoo_analyse

app = FastAPI()

app.include_router(greet)
app.include_router(retrieve)
app.include_router(preprocess)
app.include_router(analytics)
# app.include_router(visualise)
app.include_router(yahoo_analyse)

if __name__ == "__main__":
    import uvicorn  
    uvicorn.run(app, host="0.0.0.0", port=8002)
