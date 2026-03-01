from openai import OpenAI
import os

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def analyze_plant(image_path):
    # simple dummy logic (baad me upgrade karenge)
    return {
        "disease": "Leaf Spot",
        "solution": "Use neem oil spray"
    }