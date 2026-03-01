import google.generativeai as genai
import os

genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))

model = genai.GenerativeModel("gemini-1.5-flash")

def analyze_plant(image_path):
    with open(image_path, "rb") as img:
        image_data = img.read()

    response = model.generate_content([
        "Identify this plant and tell if it is healthy or diseased",
        image_data
    ])

    return response.text
