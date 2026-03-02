import google.generativeai as genai
import os

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel("gemini-2.5-flash-lite")

def analyze_plant(image_path):
    response = model.generate_content([
        """Analyze this plant and return JSON:
        {
          "status": "healthy/diseased",
          "disease": "name",
          "treatment": "solution"
        }
        """,
        {
            "mime_type": "image/jpeg",
            "data": image_bytes
        }
    ])

    return response.text

    except Exception as e:
        return f"ERROR: {str(e)}"
