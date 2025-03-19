from fastapi import FastAPI
from routes.greet import router as greet
from routes.yahoo_data import router as fetch
from routes.percentage_changes import router as percentage_change
from routes.price_chart import router as price_chart
from routes.csv_export import router as csv_export
from routes.whale_activity import router as whale_activity
from routes.moving_avg import router as moving_avg
from routes.sentiments import router as sentiments
<<<<<<< HEAD
<<<<<<< HEAD
from routes.predict import router as predict_router
from routes.preprocess import router as preprocess
=======
=======
>>>>>>> 2e29871 (Made minor changes)
# from routes.predict import router as predict_router
from routes.preprocess import router as preprocess
from routes.analytics import router as analytics
from routes.visualisation import router as visualise

>>>>>>> 2e29871 (Made minor changes)
app = FastAPI()

app.include_router(greet)
app.include_router(fetch)
app.include_router(percentage_change)
app.include_router(price_chart)
app.include_router(csv_export)
app.include_router(whale_activity)
app.include_router(moving_avg)
app.include_router(sentiments)
<<<<<<< HEAD
<<<<<<< HEAD
app.include_router(predict_router)
app.include_router(preprocess)
=======
=======
>>>>>>> 2e29871 (Made minor changes)
# app.include_router(predict_router)
app.include_router(preprocess)
app.include_router(analytics)
app.include_router(visualise)
<<<<<<< HEAD
>>>>>>> 2e29871 (Made minor changes)
=======
>>>>>>> 2e29871 (Made minor changes)

if __name__ == "__main__":
    import uvicorn  
    uvicorn.run(app, host="0.0.0.0", port=8000)
