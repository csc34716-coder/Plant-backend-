import google.generativeai as genai
import os
import json

Gemini API key

genai.configure(api_key=os.getenv(""))

model = genai.GenerativeModel("gemini-2.0-flash")

def analyze_plant(image_path, user_query=""):

with open(image_path, "rb") as f:
    image_bytes = f.read()

prompt = f"""

You are a professional plant disease expert.

Analyze the plant image carefully.

User Question: {user_query}

Return ONLY valid JSON in this format:

{{
"status":"healthy or diseased",
"disease":"name of disease or none",
"treatment":"detailed treatment and answer to the user question"
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

# remove markdown formatting if present
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
