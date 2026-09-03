from flask import Flask, request
import time

app = Flask(__name__)

@app.route("/")
def home():
    return "ESP32 Voice Server is running!"

@app.route("/upload", methods=["POST"])
def upload():

    filename = f"received_{int(time.time())}.wav"

    total = 0

    with open(filename, "wb") as f:
        while True:
            chunk = request.stream.read(4096)

            if not chunk:
                break

            f.write(chunk)
            total += len(chunk)

    print(f"Received: {filename}")
    print(f"Size: {total} bytes")

    return "WAV received successfully", 200
