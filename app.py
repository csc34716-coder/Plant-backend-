from flask import Flask
from flask_cors import CORS
from config import Config
from upload import upload_bp

app = Flask(__name__)
CORS(app)

# Load config
app.config.from_object(Config)

# Import routes


app.register_blueprint(upload_bp)

@app.route("/")
def home():
    return {"message": "Backend running 🚀"}

import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
