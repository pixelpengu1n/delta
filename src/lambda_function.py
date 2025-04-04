# src/lambda_function.py

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.routes.analytics import router as analytics_router
from src.routes.greet import router as greet_router
from src.routes.preprocess import router as preprocess_router
from src.routes.yahoo_analyse import router as yahoo_analyse_router
from src.routes.yahoo_data import router as yahoo_data_router
from src.utils.logger import configure_logging

configure_logging()

app = FastAPI()

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include all routers
app.include_router(greet_router, prefix="/api")
app.include_router(analytics_router, prefix="/api")
app.include_router(preprocess_router, prefix="/api")
app.include_router(yahoo_analyse_router, prefix="/api")
app.include_router(yahoo_data_router, prefix="/api")

# For AWS Lambda
handler = app

# For local development
if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
