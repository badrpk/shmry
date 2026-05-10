from flask import Flask, request, jsonify
import sqlite3
from pathlib import Path

app = Flask(__name__)
DB = Path.home() / "shmry_cloud_hyperscale/vault/shmry_cloud.db"
ADMIN_KEY = "shmry_admin_2026_top_secret"

@app.route('/api/dashboard')
def secure_dashboard():
    # Only allow access if the correct Admin Key is provided in headers
    key = request.headers.get('X-Admin-Key')
    if key != ADMIN_KEY:
        return jsonify({"error": "Unauthorized Access"}), 401
    
    conn = sqlite3.connect(DB)
    rows = conn.execute("""
        SELECT c.name, COUNT(i.id), SUM(t.bytes) / 1048576.0
        FROM customers c
        JOIN instances i ON c.id = i.customer_id
        LEFT JOIN telemetry t ON i.service = t.service
        GROUP BY c.name
    """).fetchall()
    conn.close()
    return jsonify([{"customer": x[0], "instances": x[1], "data_mb": round(x[2] or 0, 2)} for x in rows])

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
