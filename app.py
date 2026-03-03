from flask import Flask
from flask_cors import CORS
from config import Config
from upload import upload_bp

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "https://plant-ai-app.vercel.app"}}, supports_credentials=True)


# Load config
app.config.from_object(Config)

# Import routes


app.register_blueprint(upload_bp)

@app.route("/")
def home():
    return {"message": "Backend running 🚀"}

import os


