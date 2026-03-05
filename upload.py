from flask import Blueprint, request, jsonify
import os
import uuid
from ai_service import analyze_plant

upload_bp = Blueprint("upload", __name__)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@upload_bp.route("/upload", methods=["POST"])
def upload_image():
    # Check for image
    if 'image' not in request.files:
        return jsonify({"success": False, "error": "No image uploaded"}), 400

    # NEW: Get the user query/question from the form data
    user_query = request.form.get("user_query", "")

    file = request.files

    # Unique filename
    name = str(uuid.uuid4()) + ".jpg"
    filepath = os.path.join(UPLOAD_FOLDER, name)
    file.save(filepath)

    # AI call with error handling - Now passing user_query
    try:
        result = analyze_plant(filepath, user_query)
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

    return jsonify({
        "success": True,
        "message": "Image analyzed successfully",
        "data": result
    })
