from flask import Flask, request
from groq import Groq
import os
import time

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

    # Send WAV to Groq Whisper
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

    # Delete temporary file
    os.remove(filename)

    return "Transcription complete", 200
