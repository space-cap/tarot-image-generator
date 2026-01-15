import os
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")
API_URL = f"https://generativelanguage.googleapis.com/v1beta/models?key={API_KEY}"

print("--- Checking API Key & Listing Models ---")

try:
    response = requests.get(API_URL)
    response.raise_for_status()
    data = response.json()
    
    print(f"✅ API Access Successful!")
    print(f"Found {len(data.get('models', []))} models.")
    
    print("\nAvailable Models:")
    for model in data.get('models', []):
        name = model['name']
        methods = model.get('supportedGenerationMethods', [])
        print(f"- {name} (Methods: {methods})")
        
except Exception as e:
    print(f"❌ Error listing models: {e}")
    if hasattr(response, 'text'):
        print(f"Response Body: {response.text}")
