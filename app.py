
from flask import Flask, request, send_file
from groq import Groq
import os
import time
import glob

app = Flask(__name__)

client = Groq(api_key=os.environ["GROQ_API_KEY"])


@app.route("/")
def home():
    return "ESP32 Voice Server is running!"


@app.route("/upload", methods=["POST"])
def upload():

    filename = f"received_{int(time.time())}.wav"

    # Receive WAV from ESP32
    with open(filename, "wb") as f:
        while True:
            chunk = request.stream.read(4096)

            if not chunk:
                break

            f.write(chunk)

    print(f"Received: {filename}")
    print(f"Size: {os.path.getsize(filename)} bytes")

    # Send WAV to Groq
    print("Sending audio to Groq...")

    with open(filename, "rb") as audio_file:

        transcription = client.audio.transcriptions.create(
            file=(filename, audio_file.read()),
            model="whisper-large-v3-turbo",
            language="en",
            response_format="json",
            temperature=0
        )

    print("================================")
    print("TRANSCRIPTION:")
    print(transcription.text)
    print("================================")

    # Keep the WAV file for testing
    # os.remove(filename)

    return "Transcription complete", 200


@app.route("/download")
def download():

    files = glob.glob("received_*.wav")

    if not files:
        return "No WAV files found", 404

    # Find newest WAV
    latest = max(files, key=os.path.getmtime)

    print(f"Downloading: {latest}")

    return send_file(
        latest,
        mimetype="audio/wav",
        as_attachment=False,
        download_name=latest
    )

