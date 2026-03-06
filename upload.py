from flask import Flask, Blueprint, request, jsonify
import os
import uuid
from dotenv import load_dotenv
import cloudinary
import cloudinary.uploader
from PIL import Image  # ✅ Import PIL for image handling

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)

# Configure Cloudinary
cloudinary.config(
    cloud_name=os.getenv("CLOUD_NAME"),
    api_key=os.getenv("CLOUD_API_KEY"),
    api_secret=os.getenv("CLOUD_API_SECRET"),
)

# Blueprint setup
upload_bp = Blueprint("upload", __name__)

# Create uploads folder if it doesn't exist
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Import AI service (expects PIL.Image.Image now)
from ai_service import analyze_plant  # make sure it can accept PIL.Image.Image


@upload_bp.route("/upload", methods=["POST"])
def upload_image():
    try:
        # 1️⃣ Check if a file is included
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

        # 4️⃣ Open image as PIL and run AI analysis
        pil_image = Image.open(filepath)  # ✅ Convert to PIL.Image
        result = analyze_plant(filepath, user_query)

        # 5️⃣ Optional: delete local file to save space
        if os.path.exists(filepath):
            os.remove(filepath)

        # 6️⃣ Return result
        return jsonify({
            "success": True,
            "image_url": image_url,
            "data": result
        })

    except Exception as e:
        print("UPLOAD ERROR:", e)
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


# Register blueprint to app
app.register_blueprint(upload_bp)

# Run app standalone
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
