import google.generativeai as genai
from flask import Flask, request, jsonify

app = Flask(__name__)

genai.configure(api_key="YOUR_API_KEY")

model = genai.GenerativeModel("gemini-1.5-flash-latest")

@app.route("/", methods=["GET"])
def home():
    return "Backend running"

@app.route("/upload", methods=["POST"])
def upload():
    file = request.files['image']
    
    response = model.generate_content([
        "Describe this image",
        file.read()
    ])
    
    return jsonify({
        "message": "uploaded",
        "result": response.text
    })
