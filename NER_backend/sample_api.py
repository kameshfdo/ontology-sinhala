import requests
import json

# Define the URL and headers
url = "https://ner-server.onrender.com/api/ner"
headers = {"Content-Type": "application/json"}

# Define the data payload
data = {
    "message": "ඉන්දීය සුපිරි නළු මෝහන්ලාල් ඔහුගේ නවතම චිත්‍රපටය වන පේට්‍රියට් රූගත කිරීම් සඳහා ශ්‍රී ලංකාවට පැමිණියේ ය"
}

# Make the POST request
response = requests.post(url, headers=headers, json=data)

# Check if the request was successful
if response.status_code == 200:
    result = response.json()
    # Decode the result to convert the unicode to Sinhala characters
    decoded_result = json.dumps(result, ensure_ascii=False)
    print("API Response:", decoded_result)
else:
    print(f"Request failed with status code {response.status_code}")
