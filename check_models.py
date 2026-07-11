import os
import requests
from dotenv import load_dotenv

load_dotenv(override=True)
api_key = os.environ.get("FIREWORKS_API_KEY")

url = "https://api.fireworks.ai/inference/v1/models"
headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json"
}

print("Fetching available models...")
try:
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        models = response.json()
        print("Available Models:")
        for model in models.get("data", []):
            model_id = model.get('id')
            # Safe print to avoid unicode encoding errors on Windows console
            print(f"  - {model_id}".encode('ascii', errors='replace').decode('ascii'))
    else:
        print(f"Error: {response.status_code} - {response.text}")
except Exception as e:
    print(f"Request failed: {e}")