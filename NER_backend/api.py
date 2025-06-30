import requests
import json

# Define the URL and headers
url = "https://ner-server.onrender.com/api/ner"
headers = {"Content-Type": "application/json"}

# Define the data payload
data = {
    "message": "මහින්ද රාජපක්ෂ මහතා කොළඹට ගියේය. මහින්ද රාජපක්ෂ මහතා කොළඹට ගියේය. මහින්ද රාජපක්ෂ මහතා කොළඹට ගියේය. මහින්ද රාජපක්ෂ මහතා කොළඹට ගියේය."
}

# Function to process each message
def call_api(message):
    data = {"message": message}
    response = requests.post(url, headers=headers, json=data)
    
    if response.status_code == 200:
        result = response.json()
        decoded_result = json.dumps(result, ensure_ascii=False)
        return decoded_result
    else:
        return f"Request failed with status code {response.status_code}"
