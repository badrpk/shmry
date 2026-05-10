from flask import Flask, jsonify, render_template_string, request
import sys
from pathlib import Path

sys.path.append(str(Path.home() / "shmry_cloud_hyperscale/bin"))
from shmry_billing import generate_report
from nifdu_s3 import get_bucket_stats

app = Flask(__name__)

@app.route('/')
def index():
    return "<h1>NIFDU Sovereign Console</h1><p>Compute, Billing, and AI APIs Active.</p>"

@app.route('/api/billing')
def billing():
    return jsonify(generate_report())

@app.route('/api/predict', methods=['POST'])
def predict():
    # Mock SageMaker Inference Logic for Urdu
    data = request.get_json()
    text = data.get("text", "")
    # Sovereign AI Logic: Simple length-based mock sentiment
    sentiment = "Positive" if len(text) > 10 else "Neutral"
    return jsonify({
        "model": "NIFDU-Urdu-Llama-1",
        "input": text,
        "sentiment": sentiment,
        "region": "pk-islamabad-1"
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
