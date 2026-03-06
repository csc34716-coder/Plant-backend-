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
        dict: Always contains keys 'disease' and 'treatment'
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

Return ONLY valid JSON with keys: status, disease, treatment

Example:
{{
    "status":"healthy",
    "disease":"none",
    "treatment":"No treatment needed"
}}
"""

        # Send image + prompt to Gemini
        response = model.generate_content([prompt, image_bytes])

        text = response.text.strip()

        # Remove markdown formatting if present
        if text.startswith("```"):
            text = text.replace("```json", "").replace("```", "").strip()

        # Parse JSON response
        result = json.loads(text)

        # Ensure keys exist and match frontend
        disease = result.get("disease", "Unknown")
        treatment = result.get("treatment", "Not available")

        return {"disease": disease, "treatment": treatment}

    except Exception as e:
        # Fallback if parsing fails
        return {
            "disease": "Could not analyze image",
            "treatment": f"Error: {str(e)}"
        }
