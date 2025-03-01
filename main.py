from fastapi import FastAPI
from routes.greet import router as greet

app = FastAPI()

app.include_router(greet)

if __name__ == "__main__":
    import uvicorn  
    uvicorn.run(app, host="127.0.0.1", port=8000)
