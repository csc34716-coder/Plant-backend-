import google.generativeai as genai
import os

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel("gemini-1.5-flash")

def analyze_plant(image_path):
    try:
        with open(image_path, "rb") as img:
            image_bytes = img.read()

        response = model.generate_content([
            "Is this plant healthy or diseased? Answer in one line.",
            {
                "mime_type": "image/jpeg",
                "data": image_bytes
            }
        ])

        # SAFE RETURN
        if hasattr(response, "text"):
            return response.text
        else:
            return str(response)

    except Exception as e:
        return f"ERROR: {str(e)}"
