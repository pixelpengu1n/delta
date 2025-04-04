from fastapi import FastAPI

from src.routes.analytics import router as analytics
from src.routes.collection import router as collection
from src.routes.greet import router as greet
from src.routes.preprocess import router as preprocess
from src.routes.yahoo_analyse import router as yahoo_analyse
from src.routes.yahoo_data import router as retrieve

# from routes.visualisation import router as visualise

app = FastAPI()

# Include all routers
app.include_router(greet)
app.include_router(preprocess)
app.include_router(analytics)
app.include_router(yahoo_analyse)
app.include_router(retrieve)
app.include_router(collection)
# app.include_router(visualise)


@app.head("/")
async def head_root():
    return {}  # Return an empty response for HEAD requests


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
