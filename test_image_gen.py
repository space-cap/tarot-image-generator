import os
import requests
import base64
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")
# Using the dedicated Imagen 3 model for generation
MODEL_NAME = "imagen-4.0-fast-generate-001"
API_URL = f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL_NAME}:predict?key={API_KEY}"

print(f"Testing Image Gen with model: {MODEL_NAME}...")

# Imagen 3 specific payload format
payload = {
    "instances": [
        {
            "prompt": "Tarot card design, The Fool, mystical, detailed"
        }
    ],
    "parameters": {
        "sampleCount": 1,
        "aspectRatio": "3:4"
    }
}

try:
    print(f"POST {API_URL}")
    response = requests.post(API_URL, json=payload)
    response.raise_for_status()
    
    result = response.json()
    # Check for success
    if 'predictions' in result:
        print("✅ Success! Image generated.")
        # Optional: Save to check
        img_data = result['predictions'][0]['bytesBase64Encoded']
        with open("test_fool.png", "wb") as f:
            f.write(base64.b64decode(img_data))
        print("Saved test_fool.png")
    else:
        print("⚠️ Response received but no predictions found.")
        print(result)

except Exception as e:
    print(f"❌ Error: {e}")
    if hasattr(response, 'text'):
        print(f"Response Body: {response.text}")
