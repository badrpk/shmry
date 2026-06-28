#!/usr/bin/env python3
from flask import Flask, request, jsonify
import requests

app = Flask(__name__)
MARKETPLACE_URL = "http://127.0.0.1:5000/wa/inbound"

@app.route("/", methods=["GET"])
@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status":"healthy","gateway":"cognitive_v17","marketplace_url":MARKETPLACE_URL})

@app.route("/wa/inbound", methods=["POST"])
@app.route("/api/cognitive_commerce", methods=["POST"])
def handle_inbound():
    data = request.get_json() or {}
    text = data.get("text") or data.get("query") or data.get("message") or ""
    try:
        resp = requests.post(MARKETPLACE_URL, json={"text": text, **data}, timeout=8)
        return jsonify({"gateway":"cognitive_v17","status":"forwarded","marketplace_response":resp.json()})
    except Exception as e:
        return jsonify({"gateway":"cognitive_v17","status":"fallback","error":str(e),"reply":f"Received: {text}. Gateway fallback active."})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5060, debug=False)
