from fastapi import APIRouter, UploadFile, File, HTTPException, Query
import json
import pandas as pd
import numpy as np
import requests
from statsmodels.tsa.arima.model import ARIMA
from sklearn.ensemble import IsolationForest
from sklearn.cluster import KMeans
from textblob import TextBlob
import yfinance as yf

router = APIRouter()

# GNEWS_API_KEY = "484af3c7216b19781fcf2bc830e3628e"
# GNEWS_BASE_URL = "https://gnews.io/api/v4/search"

class DataAnalyser:
    def __init__(self, json_data):
        self.data = json_data
        self.df = self.convert_to_dataframe()
        self.dataset_categories = self.get_dataset_categories()
    
    def convert_to_dataframe(self):
        records = []
        for dataset in self.data.get("cleaned_data", []):
            for event in dataset.get("events", []):
                row = {
                    "dataset_id": dataset.get("dataset_id", "Unknown"),
                    "dataset_type": dataset.get("dataset_type", "Unknown"),
                    "event_type": event.get("event_type", "Unknown"),
                    "timestamp": event.get("time_object", {}).get("timestamp", None)  
                }
                attributes = event.get("attribute", {})
                row.update(attributes)
                records.append(row)

        df = pd.DataFrame(records)

        if "timestamp" in df.columns:
            df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce")

        return df.dropna(how='all', axis=1)  

    def get_dataset_categories(self):
        return self.df["dataset_type"].unique()
    
    def analyze_by_category(self):
        results = {}
        for category in self.dataset_categories:
            category_df = self.df[self.df["dataset_type"] == category]
            results[category] = self.generate_analysis(category_df, category)
        return results
    
    def generate_analysis(self, df, category):
        insights = {"category": category, "summary": {}}
        numeric_df = df.select_dtypes(include=[np.number]).dropna(axis=1, how='all')
        
        if not numeric_df.empty:
            insights["summary"]["statistics"] = numeric_df.describe().replace({np.nan: None}).to_dict()
            insights["anomalies"] = self.detect_anomalies(df)
            insights["patterns"] = self.detect_patterns(df)
            insights["percentage_changes"] = self.detect_percentage_changes(df)
            insights["moving_averages"] = self.calculate_moving_averages(df, window=14, method="EMA")
        
        return insights
    
    def detect_anomalies(self, df):
        if "volume" in df.columns:
            df = df[["volume"]].dropna()  
            
            if len(df) > 10:
                iso_forest = IsolationForest(contamination=0.05, random_state=42)
                df["anomaly"] = iso_forest.fit_predict(df)
                anomalies = df[df["anomaly"] == -1]
                return anomalies.to_dict(orient="records")
        
        return {}

    
    def detect_patterns(self, df):
        if "close" in df.columns:
            df = df[["close"]].dropna()
            
            if len(df) > 10:
                kmeans = KMeans(n_clusters=2, random_state=42)
                df["pattern"] = kmeans.fit_predict(df)
                return df["pattern"].value_counts().to_dict()
        return {}
    
    def detect_percentage_changes(self, df, threshold=5.0):
        if "close" in df.columns:
            df = df[["timestamp", "close"]].dropna()
            df["Pct Change"] = df["close"].pct_change() * 100
            big_events = df[abs(df["Pct Change"]) >= threshold]
            return big_events.to_dict(orient="records")
        return {}
    
    def calculate_moving_averages(self, df, window=14, method="EMA"):
        if "close" in df.columns:
            if method.upper() == "EMA":
                df[f"EMA_{window}"] = df["close"].ewm(span=window, adjust=False).mean()
            else:
                df[f"SMA_{window}"] = df["close"].rolling(window=window).mean()
            return df.to_dict(orient="records")
        return {}
    
    def run_analysis(self):
        results = self.analyze_by_category()
        return results

@router.post("/data/analyse/")
def analyze_data(file: UploadFile = File(...)):
    try:
        data = json.loads(file.file.read().decode("utf-8"))
        
        if not data.get("cleaned_data", []):
            return {"status": "success", "analysis_results": {}}
        
        analyzer = DataAnalyser(data)
        results = analyzer.run_analysis()
        return {"status": "success", "analysis_results": results}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Analysis error: {str(e)}")