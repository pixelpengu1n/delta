import json
import pandas as pd
from datetime import datetime
import numpy as np
from fastapi import APIRouter, File, UploadFile, HTTPException
import tempfile

router = APIRouter()

class DataPreprocessor:
    def __init__(self, json_data):
        self.data = self.load_json(json_data)
    
    def load_json(self, json_data):
        """Load JSON data from an uploaded file."""
        try:
            data = json.loads(json_data)
            if isinstance(data, dict):
                return [data]  # Ensure data is in list format for consistency
            return data  # Handle multiple datasets
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Error loading JSON data: {e}")
    
    def clean_data(self):
        """Perform data cleaning and standardization on the dataset."""
        cleaned_datasets = []
        for dataset in self.data:
            dataset.setdefault("events", [])  # Ensure 'events' exists
            cleaned_events = []
            
            for event in dataset.get('events', []):
                try:
                    event.setdefault("time_object", {"timestamp": datetime.now().isoformat(), "timezone": "UTC"})
                    timestamp = event['time_object'].get('timestamp', None)
                    if isinstance(timestamp, str):
                        event['time_object']['timestamp'] = self.format_timestamp(timestamp)
                    
                    event.setdefault("attribute", {})
                    event['attribute'] = self.clean_attributes(event['attribute'])
                    
                    if event not in cleaned_events:
                        cleaned_events.append(event)
                except Exception as e:
                    print(f"Error processing event: {e}")
            
            dataset['events'] = cleaned_events
            cleaned_datasets.append(dataset)
        
        return cleaned_datasets
    
    @staticmethod
    def format_timestamp(timestamp):
        """Convert timestamp to a standard format."""
        try:
            return datetime.fromisoformat(timestamp).isoformat()
        except (ValueError, TypeError):
            try:
                return datetime.strptime(timestamp, "%Y-%m-%dT%H:%M:%SZ").isoformat()
            except (ValueError, TypeError):
                return str(timestamp)
    
    @staticmethod
    def clean_attributes(attributes):
        """Handle missing values, normalize numerical data, and replace NaN with None."""
        cleaned_attributes = {}
        for k, v in attributes.items():
            if v is None or v == "":
                cleaned_attributes[k] = None  # Replace NaN with None for JSON compatibility
            elif isinstance(v, dict):
                cleaned_attributes[k] = list(v.values())[0] if v else None  # Extract nested values
            elif isinstance(v, str) and v.replace(".", "").isdigit():
                cleaned_attributes[k] = float(v)  # Convert numeric strings to float
            else:
                cleaned_attributes[k] = v
        return cleaned_attributes

@router.post("/preprocess/")
async def process_json(file: UploadFile = File(...)):
    """Endpoint to receive a JSON file, process it, and return cleaned data."""
    try:
        content = await file.read()
        json_data = content.decode("utf-8")
        preprocessor = DataPreprocessor(json_data)
        cleaned_data = preprocessor.clean_data()
        
        # Ensure NaN values are replaced with None for JSON serialization
        cleaned_data = json.loads(json.dumps(cleaned_data, default=lambda x: None if isinstance(x, float) and np.isnan(x) else x))
        
        return {"cleaned_data": cleaned_data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Processing error: {e}")