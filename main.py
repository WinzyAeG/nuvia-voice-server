from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

HUME_API_KEY = os.getenv("HUME_API_KEY")  # Inserita nelle Environment su Render

@app.route("/speak", methods=["POST"])
def speak():
    data = request.json
    text = data.get("text", "")
    emotion = data.get("emotion", "neutral")  # pronto per emozione futura

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
            "style": emotion  # usato da Hume per tono (emozione)
        }
    }

    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "X-Hume-Api-Key": HUME_API_KEY
    }

    # === DEBUG LOG UTILE ===
    print("➡️ Testo ricevuto:", text)
    print("🎭 Emozione:", emotion)
    print("📦 Payload inviato a Hume:", payload)

    try:
        res = requests.post("https://api.hume.ai/v0/octave/generate", json=payload, headers=headers)
        res.raise_for_status()
        audio_url = res.json()["audio_url"]
        return jsonify({"url": audio_url})
    except Exception as e:
        print("❌ Errore Hume:", res.status_code, res.text)
        return jsonify({"error": res.text}), res.status_code

@app.route("/", methods=["GET"])
def index():
    return "Nuvia Voice Server is running", 200
