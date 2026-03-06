from flask import Flask
from flask_cors import CORS
from upload import upload_bp
import os

app = Flask(__name__)
CORS(app)

# register upload route
app.register_blueprint(upload_bp)

@app.route("/")
def home():
    return "Plant AI Backend Running Successfully"


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)

