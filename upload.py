# upload.py
from flask import Flask, Blueprint, request, jsonify
import os
import uuid
from dotenv import load_dotenv
from PIL import Image
import cloudinary
import cloudinary.uploader

# Load environment variables from .env (local testing)
load_dotenv()

# Initialize Flask app (if not already)
app = Flask(__name__)

# Configure Cloudinary
cloudinary.config(
    cloud_name=os.getenv("CLOUD_NAME"),
    api_key=os.getenv("CLOUD_API_KEY"),
    api_secret=os.getenv("CLOUD_API_SECRET"),
)

# Blueprint setup
upload_bp = Blueprint("upload", __name__)

# Create uploads folder if not exists
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Import your AI service
from ai_service import analyze_plant  # ensure analyze_plant can accept PIL.Image.Image


@upload_bp.route("/upload", methods=["POST"])
def upload_image():
    try:
        # 1️⃣ Check if file exists in request
        if 'image' not in request.files:
            return jsonify({"success": False, "error": "No image uploaded"}), 400

        file = request.files['image']
        user_query = request.form.get("user_query", "")

        # 2️⃣ Save file temporarily
        filename = str(uuid.uuid4()) + ".jpg"
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        file.save(filepath)

        # 3️⃣ Upload to Cloudinary
        upload_result = cloudinary.uploader.upload(filepath)
        image_url = upload_result["secure_url"]

        # 4️⃣
