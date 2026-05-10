from flask import Flask, jsonify, request
import sys
from pathlib import Path

sys.path.append(str(Path.home() / "shmry_cloud_hyperscale/bin"))

from shmry_billing import generate_report
from nifdu_service_catalog import list_services, summary
try:
    from nifdu_s3 import get_bucket_stats
except Exception:
    get_bucket_stats = lambda: {"status": "S3 stats unavailable"}

app = Flask(__name__)

@app.route("/")
def index():
    s = summary()
    return f"""
    <h1>NIFDU SHMRY Sovereign Cloud</h1>
    <p>Status: ONLINE</p>
    <p>AWS-style catalog services registered: <b>{s['service_count']}</b></p>
    <ul>
      <li><a href="/api/health">/api/health</a></li>
      <li><a href="/api/catalog/summary">/api/catalog/summary</a></li>
      <li><a href="/api/services">/api/services</a></li>
      <li><a href="/api/billing">/api/billing</a></li>
      <li>/api/predict POST</li>
      <li><a href="/api/storage">/api/storage</a></li>
    </ul>
    """

@app.route("/api/health")
def health():
    return jsonify({
        "platform": "NIFDU SHMRY Sovereign Cloud",
        "region": "pk-islamabad-1",
        "status": "ONLINE"
    })

@app.route("/api/catalog/summary")
def catalog_summary():
    return jsonify(summary())

@app.route("/api/services")
def services():
    return jsonify(list_services())

@app.route("/api/service/<name>")
def service_detail(name):
    name_l = name.lower()
    for svc in list_services():
        if svc["aws_style_service"].lower() == name_l or svc["nifdu_service"].lower() == name_l:
            svc["endpoint_status"] = "stub-ready"
            svc["provisioning_status"] = "not-yet-real-infrastructure"
            return jsonify(svc)
    return jsonify({"error": "service not found", "name": name}), 404

@app.route("/api/billing")
def billing():
    return jsonify(generate_report())

@app.route("/api/storage")
def storage():
    return jsonify(get_bucket_stats())

@app.route("/api/predict", methods=["POST"])
def predict():
    data = request.get_json(silent=True) or {}
    text = data.get("text", "")
    sentiment = "Positive" if len(text) > 10 else "Neutral"
    return jsonify({
        "model": "NIFDU-Urdu-Llama-1",
        "input": text,
        "sentiment": sentiment,
        "region": "pk-islamabad-1"
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
