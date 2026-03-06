from flask import Flask
from flask_cors import CORS
from upload import upload_bp

app = Flask(__name__)
CORS(app)

# register upload route
app.register_blueprint(upload_bp)

@app.route("/")
def home():
    return "Plant AI Backend Running Successfully"


