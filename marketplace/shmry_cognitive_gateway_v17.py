from flask import Flask, request, jsonify
import sqlite3, json, traceback

app = Flask(__name__)
DB = "/home/badrpk/shmry_cloud_hyperscale/vault/shmry_cloud.db"

@app.route('/wa/inbound', methods=['POST'])
def handle_inbound():
    try:
        data = request.json
        if not data: return jsonify({"error": "Empty JSON"}), 400
        
        # Log incoming
        return jsonify({"status": "received", "gateway": "v17_active"})
    except Exception:
        return jsonify({"error": traceback.format_exc()}), 500

if __name__ == "__main__":
    app.run(port=5060, debug=False)
