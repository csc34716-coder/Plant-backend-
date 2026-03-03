import google.generativeai as genai
import os
import json

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel("gemini-2.5-flash-lite")

def analyze_plant(image_path):
    try:
        with open(image_path, "rb") as f:
            image_bytes = f.read()

        prompt = """
        Return ONLY valid JSON. No explanation.

        Format:
        {
          "status": "healthy or diseased",
          "disease": "name or none",
          "treatment": "solution"
        }
        """

        response = model.generate_content([
            prompt,
            {
                "mime_type": "image/jpeg",
                "data": image_bytes
            }
        ])

        raw_text = response.text.strip()

        # ✅ JSON parse try
        try:
            return json.loads(raw_text)
        except:
            return {
                "status": "error",
                "disease": "unknown",
                "treatment": raw_text  # fallback
            }

    except Exception as e:
        return {
            "status": "error",
            "disease": "system",
            "treatment": str(e)
        }
