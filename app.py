from flask import Flask
from flask_cors import CORS
from upload import upload_bp

app = Flask(name)
CORS(app)

register upload route

app.register_blueprint(upload_bp)

@app.route("/")
def home():
return "Plant AI Backend Running Successfully"

if name == "main":
app.run(host="0.0.0.0", port=5000)
