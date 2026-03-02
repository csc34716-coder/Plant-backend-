from flask import Blueprint, request, jsonify
import os
from ai_service import analyze_plant

upload_bp = Blueprint("upload", __name__)

UPLOAD_FOLDER = "uploads"

# ✅ IMPORTANT FIX
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@upload_bp.route("/upload", methods=["POST"])
def upload_image():
    print("HEADERS:", request.headers)
    print("FILES:", request.files)

    if 'image' not in request.files:
        return jsonify({"error": "No image"}), 400

    file = request.files['image']

    name = file.filename
    filepath = os.path.join(UPLOAD_FOLDER, name)

    file.save(filepath)

    # AI call
    result = analyze_plant(filepath)

    return jsonify({
        "message": "uploaded",
        "result": result
    })
