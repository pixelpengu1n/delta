# from fastapi import APIRouter, Query
# import yfinance as yf
# import pandas as pd
# import numpy as np
# import tensorflow as tf
# from tensorflow.keras.models import Sequential
# from tensorflow.keras.layers import LSTM, Dense
# from sklearn.preprocessing import MinMaxScaler
# from fastapi.responses import JSONResponse
# from fastapi.encoders import jsonable_encoder
# from datetime import datetime, timedelta

# router = APIRouter()

# def fetch_crypto_data(ticker: str, start_date: str, end_date: str):
#     """Fetch crypto data from Yahoo Finance."""
#     data = yf.download(ticker, start=start_date, end=end_date)
#     data = data[['Close']].reset_index()
#     data.columns = ['Date', 'Price']
#     return data

# def train_lstm_model(data: pd.DataFrame, lookback=30, future_days=30):
#     """Train an LSTM model and predict future prices."""

#     # Normalize Data
#     scaler = MinMaxScaler(feature_range=(0,1))
#     scaled_data = scaler.fit_transform(data[['Price']].values)

#     # Create training sequences
#     X_train, y_train = [], []
#     for i in range(len(scaled_data) - lookback):
#         X_train.append(scaled_data[i:i+lookback])
#         y_train.append(scaled_data[i+lookback])

#     X_train, y_train = np.array(X_train), np.array(y_train)

#     # Reshape y_train to ensure compatibility with Dense layer
#     y_train = y_train.reshape(-1, 1)

#     # Build LSTM Model
#     model = Sequential([
#         LSTM(50, activation='relu', return_sequences=True, input_shape=(lookback, 1)),
#         LSTM(50, activation='relu', return_sequences=False),  # Last LSTM should not return sequences
#         Dense(1)
#     ])

#     model.compile(optimizer='adam', loss='mean_squared_error')

#     # Train the model
#     model.fit(X_train, y_train, epochs=10, batch_size=16, verbose=1)

#     # Generate future predictions
#     last_sequence = scaled_data[-lookback:].reshape(1, lookback, 1)
#     predictions = []

#     for _ in range(future_days):
#         predicted_price = model.predict(last_sequence)
#         predictions.append(predicted_price[0][0])
#         last_sequence = np.append(last_sequence[:, 1:, :], [[[predicted_price[0][0]]]], axis=1)

#     # Convert predictions back to original scale
#     predictions = scaler.inverse_transform(np.array(predictions).reshape(-1, 1)).flatten().tolist()

#     return predictions

# @router.get("/predict/lstm/")
# def predict(
#     ticker: str = Query(..., description="The crypto ticker symbol."),
#     start_date: str = Query(..., description="Start date for training (YYYY-MM-DD)."),
#     end_date: str = Query(..., description="End date for training (YYYY-MM-DD)."),
#     future_days: int = Query(30, description="Number of days to predict.")
# ):
#     """Predict future crypto prices using an LSTM model."""

#     # Fetch historical crypto data
#     data = fetch_crypto_data(ticker, start_date, end_date)

#     if data.empty:
#         return JSONResponse(content={"error": "No data found."}, status_code=404)

#     predictions = train_lstm_model(data, lookback=30, future_days=future_days)

#     # Generate future dates starting from end_date
#     last_known_date = datetime.strptime(end_date, "%Y-%m-%d")
#     future_dates = [(last_known_date + timedelta(days=i)).strftime("%Y-%m-%d") for i in range(1, future_days + 1)]

#     # Format output with dates
#     labeled_predictions = [{"date": date, "price": price} for date, price in zip(future_dates, predictions)]

#     return JSONResponse(content=jsonable_encoder({"predictions": labeled_predictions}))
