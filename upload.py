from flask import Blueprint, request, jsonify
import os
import uuid
from ai_service import analyze_plant

upload_bp = Blueprint("upload", __name__)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@upload_bp.route("/upload", methods=["POST"])
def upload_image():
    if 'image' not in request.files:
        return jsonify({"error": "No image"}), 400

    file = request.files['image']

    # Unique filename
    name = str(uuid.uuid4()) + ".jpg"
    filepath = os.path.join(UPLOAD_FOLDER, name)

    file.save(filepath)

    # AI call with error handling
    try:
        result = analyze_plant(filepath)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

    return jsonify({
        "success": True,
        "message": "Image analyzed successfully",
        "data": result
    })
