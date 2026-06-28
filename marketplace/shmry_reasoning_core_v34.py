from flask import Flask, request, jsonify
import os, subprocess, json
from pathlib import Path

app = Flask(__name__)

@app.route("/ai/chat", methods=["POST"])
def chat():
    msg = request.json.get("msg", "Say SHMRY is alive.")
    try:
        # Call the executor as a separate process to release memory immediately
        result = subprocess.check_output(
            ["/home/badrpk/shmry_env/bin/python", "/home/badrpk/shmry_ai_executor.py", msg],
            env=os.environ
        )
        return jsonify({"ok": True, "reply": result.decode().strip()})
    except Exception as e:
        return jsonify({"ok": False, "error": str(e)})

@app.get("/health")
def health():
    return jsonify({"ok": True, "mode": "subprocess_safe"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5060)
