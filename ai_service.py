import requests
import os
import base64

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

def analyze_plant(image_path):
    url = f"https://generativelanguage.googleapis.com/v1/models/gemini-1.5-flash-latest:generateContent?key={GEMINI_API_KEY}"

    with open(image_path, "rb") as img:
        image_data = img.read()

    base64_image = base64.b64encode(image_data).decode("utf-8")

    data = {
        "contents": [{
            "parts": [
                {"text": "Is this plant healthy or diseased? Answer in one line."},
                {
                    "inline_data": {
                        "mime_type": "image/jpeg",
                        "data": base64_image
                    }
                }
            ]
        }]
    }

    response = requests.post(url, json=data)

    try:
        return response.json()["candidates"][0]["content"]["parts"][0]["text"]
    except:
        return response.text
