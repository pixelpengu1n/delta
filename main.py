from fastapi import FastAPI
from routes.greet import router as greet
from routes.preprocess import router as preprocess
from routes.analytics import router as analytics
# from routes.visualisation import router as visualise
from routes.collection import router as collection

app = FastAPI()

app.include_router(greet)
app.include_router(preprocess)
app.include_router(analytics)
# app.include_router(visualise)
app.include_router(collection)

@app.head("/")
async def head_root():
    return {}  # Return an empty response for HEAD requests

if __name__ == "__main__":
    import uvicorn  
    uvicorn.run(app, host="127.0.0.1", port=8001)
