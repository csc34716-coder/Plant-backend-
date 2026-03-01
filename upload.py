from flask import Blueprint, request, jsonify
import os


upload_bp = Blueprint("upload", __name__)

UPLOAD_FOLDER = "uploads"

@upload_bp.route("/upload", methods=["POST"])
def upload_image():

    if 'image' not in request.files:
        return jsonify({"error": "No image"}),400

    file = request.files['image']

    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)

    name = file.filename
    filepath = f"{UPLOAD_FOLDER}/{name}"

    file.save(filepath)
    

    return jsonify({
    "message": "uploaded"})
from ai_service import analyze_plant

@app.route("/upload", methods=["POST"])
def upload():
    file = request.files["file"]

    filepath = "temp.jpg"
    file.save(filepath)

    result = analyze_plant(filepath)

    return {"result": result}
