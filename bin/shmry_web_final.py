from flask import Flask, request, render_template_string, jsonify
import sqlite3, uuid, time
from pathlib import Path

app = Flask(__name__)
DB = Path.home() / "shmry_cloud_hyperscale/vault/shmry_cloud.db"

@app.route('/')
def index():
    return "<h1>NIFDU.COM IS ONLINE</h1><p>Sovereign Cloud Gateway Active.</p>"

@app.route('/api/health')
def health():
    return jsonify({"status": "ONLINE", "region": "Islamabad-A", "platform": "SHMRY"})

@app.route('/api/dashboard')
def dashboard():
    conn = sqlite3.connect(DB)
    rows = conn.execute("SELECT name, tier FROM customers").fetchall()
    conn.close()
    return jsonify([{"name": r[0], "tier": r[1]} for r in rows])

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
