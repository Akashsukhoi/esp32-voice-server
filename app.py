from flask import Flask, request, send_file
import time
import os

app = Flask(__name__)

@app.route("/")
def home():
    return "ESP32 Voice Server is running!"

@app.route("/upload", methods=["POST"])
def upload():
    filename = f"received_{int(time.time())}.wav"

    with open(filename, "wb") as f:
        while True:
            chunk = request.stream.read(4096)
            if not chunk:
                break
            f.write(chunk)

    size = os.path.getsize(filename)

    print(f"Received: {filename}")
    print(f"Size: {size} bytes")

    return "WAV received successfully", 200

@app.route("/download")
def download():
    files = [f for f in os.listdir(".") if f.endswith(".wav")]

    if not files:
        return "No WAV file found", 404

    latest = max(files, key=os.path.getmtime)
    return send_file(latest, mimetype="audio/wav")
