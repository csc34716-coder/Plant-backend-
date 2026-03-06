import google.generativeai as genai
import os
import json

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel("gemini-1.5-flash")

def analyze_plant(image_path, user_query=""):

    with open(image_path, "rb") as f:
        image_bytes = f.read()

    prompt = f"""
You are a professional plant disease expert.

Analyze the plant image carefully.

User Question: {user_query}

Return ONLY valid JSON:

{{
"status":"healthy or diseased",
"disease":"name of disease or none",
"treatment":"detailed treatment"
}}
"""

    response = model.generate_content([prompt, image_bytes])

    text = response.text.strip()

    if text.startswith("```"):
        text = text.replace("```json", "").replace("```", "").strip()

    try:
        return json.loads(text)
    except:
        return {
            "status": "error",
            "disease": "unknown",
            "treatment": text
        }
