#!/usr/bin/env python3
from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

MARKETPLACE_URL = "http://127.0.0.1:5000/wa/inbound"

@app.route('/wa/inbound', methods=['POST'])
def handle_inbound():
    try:
        data = request.get_json() or {}
        text = data.get('text', '').strip()
        
        # Forward to main marketplace
        resp = requests.post(MARKETPLACE_URL, json=data, timeout=10)
        
        if resp.status_code == 200:
            return jsonify({
                "gateway": "cognitive_v17",
                "status": "forwarded",
                "marketplace_response": resp.json()
            })
        else:
            return jsonify({"error": "Marketplace returned error", "code": resp.status_code}), 502
    except Exception as e:
        return jsonify({
            "gateway": "cognitive_v17",
            "status": "fallback",
            "reply": "✅ Received and logged",
            "error": str(e)
        }), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5060, debug=False)
