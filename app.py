from flask import Flask, request
import os
import time

app = Flask(__name__)

@app.route("/")
def home():
    return "ESP32 Voice Server is running!"

@app.route("/upload", methods=["POST"])
def upload():

    if not request.data:
        return "No audio received", 400

    filename = f"received_{int(time.time())}.wav"

    with open(filename, "wb") as f:
        f.write(request.data)

    print(f"Received WAV: {filename}")
    print(f"Size: {len(request.data)} bytes")

    return "WAV received successfully", 200


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)