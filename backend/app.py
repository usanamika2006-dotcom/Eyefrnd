from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import cv2
import numpy as np
import os
import sys

# OpenBLAS fix for some windows environments
os.environ["OPENBLAS_NUM_THREADS"] = "1"

from state import app_state
from services.face_clean_service import detect_face_clean
from services.description_service import describe_person
# from services.voice_service import speak # Removed server-side speech
# Use absolute path for static folder to avoid CWD issues
base_dir = os.path.dirname(os.path.abspath(__file__))
frontend_dir = os.path.join(base_dir, "..", "frontend")

# Initialize Flask without default static folder to allow manual control
app = Flask(__name__, static_folder=None)
CORS(app) # Enable CORS for all routes

@app.route("/")
def home():
    print(f"Request for / - Serving index.html from {frontend_dir}")
    if not os.path.exists(os.path.join(frontend_dir, "index.html")):
        return "Index file not found", 404
    return send_from_directory(frontend_dir, "index.html")

@app.route("/<path:path>")
def static_files(path):
    print(f"Request for {path} - Serving from {frontend_dir}")
    return send_from_directory(frontend_dir, path)

@app.route("/start")
def start():
    app_state.current_mode = "idle"
    message = "Hello Friend. Choose a mode."
    # speak(message) # Client handle speech
    return jsonify({"message": message})


@app.route("/voice-command", methods=["POST"])
def voice_command():

    command = request.json.get("command", "").lower()

    if "face" in command:
        app_state.current_mode = "face"
        response = "Face clean mode activated."
    elif "description" in command:
        app_state.current_mode = "description"
        response = "Description mode activated."
    elif "bye" in command:
        app_state.current_mode = "idle"
        response = "Goodbye Friend."
    else:
        response = "Command not recognized."

    # speak(response)
    return jsonify({"message": response})


@app.route("/scan", methods=["POST"])
def scan():

    # Relaxed check: we can just process it even if mode isn't explicitly set, 
    # unless we want to enforce state. For a better UX, we'll allow it.
    app_state.current_mode = "face" 

    if "image" not in request.files:
        return jsonify({"message": "No image uploaded"}), 400

    file = request.files["image"]
    npimg = np.frombuffer(file.read(), np.uint8)
    image = cv2.imdecode(npimg, cv2.IMREAD_COLOR)

    result = detect_face_clean(image, app_state.ignored_regions)
    # speak(result)

    return jsonify({"message": result})


@app.route("/describe", methods=["POST"])
def describe():

    app_state.current_mode = "description"

    if "image" not in request.files:
         return jsonify({"message": "No image uploaded"}), 400

    file = request.files["image"]
    npimg = np.frombuffer(file.read(), np.uint8)
    image = cv2.imdecode(npimg, cv2.IMREAD_COLOR)

    result = describe_person(image)
    # speak(result)

    return jsonify({"message": result})


if __name__ == "__main__":
    app.run(debug=True, port=5000)
