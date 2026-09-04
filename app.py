from flask import Flask, request
from openai import OpenAI
import os
import time

app = Flask(__name__)

client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])


@app.route("/")
def home():
    return "ESP32 Voice Server is running!"


@app.route("/upload", methods=["POST"])
def upload():

    filename = f"received_{int(time.time())}.wav"

    # Save incoming WAV
    with open(filename, "wb") as f:
        while True:
            chunk = request.stream.read(4096)

            if not chunk:
                break
                

            f.write(chunk)

    size = os.path.getsize(filename)

    print(f"Received: {filename}")
    print(f"Size: {size} bytes")

    # Send WAV to OpenAI
    print("Sending audio to OpenAI...")

    with open(filename, "rb") as audio_file:

        transcription = client.audio.transcriptions.create(
            model="gpt-4o-mini-transcribe",
            file=audio_file
        )

    print("================================")
    print("TRANSCRIPTION:")
    print(transcription.text)
    print("================================")

    # Delete temporary WAV
    os.remove(filename)

    return "Transcription complete", 200
