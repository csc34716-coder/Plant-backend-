import google.generativeai as genai
import os

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel("Gemini 2.5 Flash-Lite")

def analyze_plant(image_path):
    try:
        with open(image_path, "rb") as img:
            image_bytes = img.read()

        response = model.generate_content([
            "Tell in one line: healthy or diseased plant.",
            {
                "mime_type": "image/jpeg",
                "data": image_bytes
            }
        ])

        return response.text

    except Exception as e:
        return f"ERROR: {str(e)}"
