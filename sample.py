import requests
import json

# AWS API Gateway Endpoints
PREPROCESS_URL = "https://h0gn7fm71g.execute-api.ap-southeast-2.amazonaws.com/dev/preprocess"
ANALYSE_URL = "https://h0gn7fm71g.execute-api.ap-southeast-2.amazonaws.com/dev/analyse"

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

# Convert JSON data to string and send to AWS API Gateway for preprocessing
preprocess_response = requests.post(
    PREPROCESS_URL,
    headers={"Content-Type": "application/json"},
    data=json.dumps(retrieved_data)
)

if preprocess_response.status_code == 200:
    preprocessed_data = preprocess_response.json()  # Convert response to dictionary
    print("Preprocessed Data Received:", json.dumps(preprocessed_data, indent=4))
    
    # Send preprocessed data directly to analysis endpoint
    analyse_response = requests.post(
        ANALYSE_URL,
        headers={"Content-Type": "application/json"},
        data=json.dumps(preprocessed_data)
    )
    
    if analyse_response.status_code == 200:
        analysed_data = analyse_response.json()
        print("Analysed Data Received:", json.dumps(analysed_data, indent=4))
    else:
        print(f"Error during analysis: {analyse_response.status_code}, {analyse_response.text}")
else:
    print(f"Error during preprocessing: {preprocess_response.status_code}, {preprocess_response.text}")
