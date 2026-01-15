import os
import requests
import json
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")
MODEL_NAME = "gemini-2.0-flash-exp"
API_URL = f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL_NAME}:generateContent?key={API_KEY}"

payload = {
    "contents": [{
        "parts": [{"text": "Draw a picture of a tarot card. output the image."}]
    }]
}

print(f"Asking {MODEL_NAME} to draw...")
try:
    response = requests.post(API_URL, json=payload)
    print(f"Status: {response.status_code}")
    print(response.text)
except Exception as e:
    print(e)
