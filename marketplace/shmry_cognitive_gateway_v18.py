from flask import Flask, request, jsonify
import sqlite3
from pathlib import Path

app = Flask(__name__)
DB = str(Path.home() / "shmry_cloud_hyperscale/vault/shmry_cloud.db")

@app.route('/wa/inbound', methods=['POST'])
def handle_inbound():
    data = request.json
    if not data: return jsonify({"error": "No JSON"}), 400
    
    # Simple acknowledgement to verify route
    return jsonify({"reply": "🧠 Gateway v18 Online and Processing"})

if __name__ == "__main__":
    app.run(port=5060, debug=False)
