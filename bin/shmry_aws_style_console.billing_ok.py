from flask import Flask, jsonify, render_template_string
import sqlite3
import sys
from pathlib import Path

# Add bin to path so we can import shmry_billing
sys.path.append(str(Path.home() / "shmry_cloud_hyperscale/bin"))
from shmry_billing import generate_report

app = Flask(__name__)
DB = Path.home() / "shmry_cloud_hyperscale/vault/shmry_cloud.db"

@app.route('/')
def index():
    return "<h1>NIFDU Console</h1><p>Billing and Compute APIs Active.</p>"

@app.route('/api/billing')
def billing_api():
    return jsonify(generate_report())

@app.route('/api/health')
def health():
    return jsonify({"status": "ONLINE", "region": "Islamabad-A"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
