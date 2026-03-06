# ai_service.py
import google.generativeai as genai
import os
import json

# Configure Gemini API key
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Initialize model
model = genai.GenerativeModel("gemini-1.5-flash")

def analyze_plant(image_path: str, user_query: str = "") -> dict:
    """
    Analyze a plant image using Google Gemini AI.
    
    Args:
        image_path (str): Path to the image file.
        user_query (str): Optional user question about the plant.
        
    Returns:
        dict: JSON-compatible dictionary with keys:
            - status: "healthy" or "diseased"
            - disease: disease name or "none"
            - treatment: recommended treatment
    """
    try:
        # Read image bytes
        with open(image_path, "rb") as f:
            image_bytes = f.read()

        # Create prompt
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

        # Send image + prompt to Gemini
        response = model.generate_content([prompt, image_bytes])

        text = response.text.strip()

        # Remove markdown formatting if present
        if text.startswith("```"):
            text = text.replace("```json", "").replace("```", "").strip()

        # Parse JSON response
        return json.loads(text)

    except Exception as e:
        # Fallback if parsing fails
        return {
            "status": "error",
            "disease": "unknown",
            "treatment": f"Could not analyze image: {str(e)}"
        }
