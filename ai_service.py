import google.generativeai as genai
import os
import json

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel("gemini-1.5-flash")

def analyze_plant(image_path, user_query=""):

    with open(image_path, "rb") as f:
        image_bytes = f.read()

    prompt = f"""
Return ONLY valid JSON.

You are a plant disease expert.

User Question: {user_query}

Analyze the plant and respond in JSON:

{{
"status":"healthy or diseased",
"disease":"name of disease or none",
"treatment":"detailed treatment and answer to user question"
}}
"""

    response = model.generate_content([
        prompt,
        {
            "mime_type": "image/jpeg",
            "data": image_bytes
        }
    ])

    text = response.text.strip()

    if text.startswith("```"):
        text = text.replace("```json","").replace("```","")

    try:
        return json.loads(text)
    except:
        return {
            "status":"error",
            "disease":"unknown",
            "treatment":text
        }
