from fastapi import APIRouter, UploadFile, File, HTTPException, Response
import json
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import io

router = APIRouter()

class DataVisualiser:
    def __init__(self, json_data):
        self.data = json_data
        self.df = self.convert_to_dataframe()
    
    def convert_to_dataframe(self):
        records = []
        for dataset in self.data.get("cleaned_data", []):
            for event in dataset.get("events", []):
                row = {
                    "dataset_id": dataset.get("dataset_id", "Unknown"),
                    "dataset_type": dataset.get("dataset_type", "Unknown"),
                    "event_type": event.get("event_type", "Unknown"),
                    "timestamp": event.get("time_object", {}).get("timestamp", None),
                }
                attributes = event.get("attribute", {})
                row.update(attributes)
                records.append(row)
        
        df = pd.DataFrame(records)
        
        # Convert timestamp column to datetime
        if "timestamp" in df.columns:
            df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce")
        
        return df.dropna(how="all", axis=1)

    def plot_time_series(self):
        """Plot a time series graph for numeric attributes over time."""
        numeric_cols = self.df.select_dtypes(include=[np.number]).columns
        if "timestamp" in self.df.columns and not self.df.empty:
            plt.figure(figsize=(10, 5))
            for col in numeric_cols:
                plt.plot(self.df["timestamp"], self.df[col], label=col)

            plt.xlabel("Time")
            plt.ylabel("Value")
            plt.legend()
            plt.title("Time Series Data")
            return self._save_plot()
        return None

    def plot_histogram(self):
        """Plot histograms for numeric attributes."""
        numeric_cols = self.df.select_dtypes(include=[np.number]).columns
        if not numeric_cols.empty:
            plt.figure(figsize=(10, 5))
            for col in numeric_cols:
                plt.hist(self.df[col].dropna(), bins=15, alpha=0.6, label=col)

            plt.xlabel("Value")
            plt.ylabel("Frequency")
            plt.legend()
            plt.title("Histogram of Numeric Data")
            return self._save_plot()
        return None

    def plot_scatter_matrix(self):
        """Plot a scatter matrix for numeric variables."""
        numeric_cols = self.df.select_dtypes(include=[np.number])
        if not numeric_cols.empty and len(numeric_cols.columns) > 1:
            pd.plotting.scatter_matrix(numeric_cols, figsize=(10, 10), diagonal="kde")
            return self._save_plot()
        return None

    def _save_plot(self):
        """Save the current Matplotlib figure to a memory buffer."""
        buf = io.BytesIO()
        plt.savefig(buf, format="png")
        plt.close()
        buf.seek(0)
        return buf

@router.post("/visualise/")
def visualise_data(file: UploadFile = File(...)):
    try:
        data = json.loads(file.file.read().decode("utf-8"))
        visualiser = DataVisualiser(data)

        # Choose which graph to return
        img_buffer = visualiser.plot_time_series()
        if img_buffer is None:
            img_buffer = visualiser.plot_histogram()
        if img_buffer is None:
            img_buffer = visualiser.plot_scatter_matrix()

        if img_buffer:
            return Response(content=img_buffer.read(), media_type="image/png")
        else:
            raise HTTPException(status_code=400, detail="No suitable visualisation available.")

    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Visualisation error: {str(e)}")
