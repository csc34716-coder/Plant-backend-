import google.generativeai as genai
import os
import json

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Note: Using gemini-1.5-flash or gemini-2.0-flash is recommended for best results
model = genai.GenerativeModel("gemini-1.5-flash")

def analyze_plant(image_path, user_query=""): # Added user_query parameter
    try:
        with open(image_path, "rb") as f:
            image_bytes = f.read()

        # Updated prompt to include the User Question
        prompt = f"""
        Return ONLY valid JSON. No explanation.

        Context: You are a professional botanist. 
        User Question: {user_query}

        Instructions:
        1. Analyze the plant health from the image.
        2. Specifically address the User Question in the 'treatment' section.
        
        Format:
        {{
          "status": "healthy or diseased",
          "disease": "name of disease or none",
          "treatment": "detailed solution and answer to the user question"
        }}
        """

        response = model.generate_content([
            prompt,
            {
                "mime_type": "image/jpeg",
                "data": image_bytes
            }
        ])

        raw_text = response.text.strip()

        # ✅ REMOVE ```json and ```
        if raw_text.startswith("```"):
            raw_text = raw_text.replace("```json", "").replace("```", "").strip()
        
        print("CLEAN AI:", raw_text)
        
        # ✅ JSON parse try
        try:
            return json.loads(raw_text)
        except:
            return {
                "status": "error",
                "disease": "parsing_error",
                "treatment": raw_text  # fallback
            }

    except Exception as e:
        return {
            "status": "error",
            "disease": "system_error",
            "treatment": str(e)
        }

