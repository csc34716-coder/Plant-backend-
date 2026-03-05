from flask import Flask, request, jsonify
from flask_cors import CORS
import cloudinary
import cloudinary.uploader
import tempfile
import os
from ai_service import analyze_plant

app = Flask(__name__)
CORS(app)

# Cloudinary config
cloudinary.config(
    cloud_name=os.getenv("CLOUDINARY_CLOUD_NAME"),
    api_key=os.getenv("CLOUDINARY_API_KEY"),
    api_secret=os.getenv("CLOUDINARY_API_SECRET")
)

@app.route("/")
def home():
    return "Plant AI backend running"

@app.route("/analyze", methods=["POST"])
def analyze():

    image = request.files.get("image")
    user_query = request.form.get("query")

    if not image:
        return jsonify({"error": "No image uploaded"})

    # save temporary file
    temp = tempfile.NamedTemporaryFile(delete=False)
    image.save(temp.name)

    # AI analysis
    result = analyze_plant(temp.name, user_query)

    # upload to cloudinary
    upload = cloudinary.uploader.upload(temp.name)

    image_url = upload["secure_url"]

    return jsonify({
        "status": result.get("status"),
        "disease": result.get("disease"),
        "treatment": result.get("treatment"),
        "image_url": image_url
    })


if __name__ == "__main__":
    app.run()
