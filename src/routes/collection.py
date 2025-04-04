import uuid
from datetime import datetime
from typing import Optional

import pandas as pd
from fastapi import APIRouter, File, HTTPException, Query, UploadFile

router = APIRouter()


@router.post("/collect/")
async def collect_csv_data(
    file: UploadFile = File(...),
    data_source: str = Query("generic_source"),
    dataset_type: str = Query("generic"),
    timestamp_column: str = Query("timestamp"),
    event_type_column: Optional[str] = Query(None),
    duration: int = Query(1),
    duration_unit: str = Query("day"),
    timezone: str = Query("UTC"),
):
    """
    Endpoint to receive a CSV file and return a structured AGADE JSON object.
    """
    try:
        # Read uploaded CSV content
        content = await file.read()
        df = pd.read_csv(pd.io.common.BytesIO(content))

        # Convert DataFrame rows to AGADE-compliant events
        events = []
        for _, row in df.iterrows():
            timestamp_val = row.get(timestamp_column)
            if pd.isna(timestamp_val):
                continue  # Skip rows without valid timestamps

            try:
                formatted_ts = pd.to_datetime(str(timestamp_val)).isoformat() + "+00:00"
            except Exception:
                formatted_ts = str(timestamp_val)

            event_type = (
                row.get(event_type_column)
                if event_type_column and event_type_column in row
                else "generic_event"
            )

            # Filter out known metadata columns from attributes
            attribute = {
                k: (None if pd.isna(v) or v == "" else v)
                for k, v in row.items()
                if k not in [timestamp_column, event_type_column]
            }

            events.append(
                {
                    "time_object": {
                        "timestamp": formatted_ts,
                        "duration": duration,
                        "duration_unit": duration_unit,
                        "timezone": timezone,
                    },
                    "event_type": str(event_type),
                    "attribute": attribute,
                }
            )

        # Create final AGADE-formatted dataset
        dataset_id = str(uuid.uuid4())
        now = datetime.utcnow().isoformat() + "Z"
        agade_dataset = {
            "data_source": data_source,
            "dataset_type": dataset_type,
            "dataset_id": dataset_id,
            "time_object": {"timestamp": now, "timezone": "UTC"},
            "events": events,
        }

        return agade_dataset

    except pd.errors.EmptyDataError:
        raise HTTPException(status_code=400, detail="CSV file is empty or invalid.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing CSV: {str(e)}")
