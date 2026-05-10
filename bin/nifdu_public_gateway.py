from flask import Flask, jsonify, render_template_string
import sqlite3
from pathlib import Path

app = Flask(__name__)
DB_PATH = Path.home() / "shmry_cloud_hyperscale/vault/shmry_cloud.db"

def get_services():
    with sqlite3.connect(DB_PATH) as conn:
        conn.row_factory = sqlite3.Row
        return [dict(row) for row in conn.execute("SELECT * FROM services").fetchall()]

@app.route('/')
def home():
    services = get_services()
    return render_template_string("""
        <h1>NIFDU Sovereign Cloud Gateway</h1>
        <p>Status: ONLINE | Node: pk-islamabad-1</p>
        <ul>
            {% for s in services %}
            <li><strong>{{ s.aws_style_service }}</strong>: {{ s.status }} ({{ s.nifdu_service }})</li>
            {% endfor %}
        </ul>
    """, services=services)

@app.route('/api/v1/services')
def api_services():
    return jsonify({"platform": "NIFDU", "services": get_services()})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
