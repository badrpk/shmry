from flask import Flask, jsonify, request
import subprocess
import json

app = Flask(__name__)

# Simple security check to match your environment's requirements
@app.before_request
def check_token():
    if request.headers.get('X-NIFDU-Token') != 'EVOLVE_2026':
        return jsonify({"error": "unauthorized", "hint": "Send X-NIFDU-Token header"}), 401

@app.route('/pulse')
def pulse():
    result = subprocess.run(
        ['/home/badrpk/shmry_cloud_hyperscale/bin/perception_buffer', 'HEALTH_CHECK'],
        capture_output=True, text=True
    )
    try:
        data = json.loads(result.stdout)
        return jsonify(data)
    except Exception as e:
        return jsonify({"error": "NIFDU_CORE_OFFLINE", "details": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
