from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

HUME_API_KEY = os.getenv("HUME_API_KEY")

@app.route("/speak", methods=["POST"])
def speak():
    data = request.json
    text = data.get("text", "")
    emotion = data.get("emotion", "neutral")

    print("🔎 Testo ricevuto dal client:", text)
    print("📏 Lunghezza dopo strip:", len(text.strip()))

    if not text or len(text.strip()) < 5:
        return jsonify({"error": "Testo troppo breve per generare voce"}), 400

    payload = {
        "text": text,
        "voice": {
            "name": "emma",
            "language": "it"
        },
        "prosody": {
            "rate": 1.0,
            "pitch": 1.0
        },
        "modulation": {
            "style": emotion
        }
    }

    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "X-Hume-Api-Key": HUME_API_KEY
    }

    print("🎭 Emozione:", emotion)
    print("📦 Payload inviato a Hume:", payload)

    res = requests.post("https://api.hume.ai/v0/octave/generate", json=payload, headers=headers)
    print("📡 Risposta Hume:", res.status_code, res.text)

    if res.status_code == 200:
        audio_url = res.json().get("audio_url")
        if audio_url:
            return jsonify({"url": audio_url})
        else:
            return jsonify({"error": "Audio URL mancante nella risposta Hume"}), 502
    else:
        return jsonify({"error": res.text}), res.status_code

@app.route("/", methods=["GET"])
def index():
    return "Nuvia Voice Server is running", 200
