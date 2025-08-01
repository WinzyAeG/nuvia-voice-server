from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

HUME_API_KEY = os.getenv("HUME_API_KEY")  # da impostare su Render

@app.route("/speak", methods=["POST"])
def speak():
    data = request.json
    text = data.get("text", "")
    
    # Configura l'emozione (opzionale)
    payload = {
        "text": text,
        "voice": {
            "name": "emma",   # Voce Hume
            "language": "it"
        },
        "prosody": {
            "rate": 1.0,
            "pitch": 1.0
        }
    }

    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "X-Hume-Api-Key": HUME_API_KEY
    }

    res = requests.post("https://api.hume.ai/v0/octave/generate", json=payload, headers=headers)

    if res.status_code == 200:
        audio_url = res.json()["audio_url"]
        return jsonify({"url": audio_url})
    else:
        return jsonify({"error": res.text}), res.status_code

@app.route("/", methods=["GET"])
def index():
    return "Nuvia Voice Server is running", 200
