import requests
import json

# AWS API Gateway Endpoint
API_URL = "https://h0gn7fm71g.execute-api.ap-southeast-2.amazonaws.com/dev/preprocess"

# Retrieved JSON data (example)
retrieved_data = [
    {
        "data_source": "EuroFidai",
        "dataset_type": "ESG",
        "dataset_id": "Aspen_Pharmacare_Holdings_Ltd_G_unit_test_subset",
        "time_object": {
            "timestamp": "2025-03-10T12:34:56Z",
            "timezone": "GMT+11"
        },
        "events": [
            {
                "time_object": {
                    "timestamp": "2017-12-31T00:00:00",
                    "duration": 0,
                    "timezone": "GMT+0"
                },
                "event_type": "ANALYTICEMPLOYMENTCREATION",
                "attribute": {
                    "company": "Aspen Pharmacare Holdings Ltd",
                    "metric_value": "-2.94"
                }
            }
        ]
    }
]

# Convert JSON data to string and send to AWS API Gateway
response = requests.post(
    API_URL,
    headers={"Content-Type": "application/json"},
    data=json.dumps(retrieved_data)  # Convert Python object to JSON string
)

# Get the response data
if response.status_code == 200:
    preprocessed_data = response.json()  # Convert response to dictionary
    print("Preprocessed Data Received:", json.dumps(preprocessed_data, indent=4))
else:
    print(f"Error: {response.status_code}, {response.text}")
