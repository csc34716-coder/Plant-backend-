from flask import Blueprint, request, jsonify
import os
import uuid
import cloudinary
import cloudinary.uploader
from ai_service import analyze_plant

upload_bp = Blueprint("upload", __name__)

# Cloudinary config
cloudinary.config(
    cloud_name=os.getenv("CLOUDINARY_CLOUD_NAME"),
    api_key=os.getenv("CLOUDINARY_API_KEY"),
    api_secret=os.getenv("CLOUDINARY_API_SECRET")
)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


@upload_bp.route("/upload", methods=["POST"])
def upload_image():

    if 'image' not in request.files:
        return jsonify({"success": False, "error": "No image uploaded"}), 400

    file = request.files['image']

    # user query from frontend
    user_query = request.form.get("user_query", "")

    # save temporary
    filename = str(uuid.uuid4()) + ".jpg"
    filepath = os.path.join(UPLOAD_FOLDER, filename)

    file.save(filepath)

    try:
        # upload to cloudinary
        upload_result = cloudinary.uploader.upload(filepath)
        image_url = upload_result["secure_url"]

        # AI analysis
        result = analyze_plant(filepath, user_query)

        return jsonify({
            "success": True,
            "image_url": image_url,
            "data": result
        })

    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500
