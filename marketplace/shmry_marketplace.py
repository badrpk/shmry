from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)
DB = "/home/badrpk/shmry_cloud_hyperscale/vault/shmry_cloud.db"

@app.route('/wa/inbound', methods=['POST'])
def handle_inbound():
    data = request.json
    user_input = data.get("text", "").strip()
    
    db = sqlite3.connect(DB)
    # Check for active clarification session
    active = db.execute("SELECT session_id FROM shmry_demand_sessions WHERE status='CLARIFYING' ORDER BY id DESC LIMIT 1").fetchone()
    
    if active:
        sid = active[0]
        # Append answer to session and transition status
        db.execute("UPDATE shmry_demand_sessions SET captured_fields = captured_fields || ?, status='PROCESSING' WHERE session_id=?", (f"|{user_input}", sid))
        db.commit()
        return jsonify({"reply": f"🧠 Updating session {sid} with: {user_input}..."})
    
    # Fallback to router logic
    return jsonify({"reply": "✨ SHMRY Router: Ready."})

if __name__ == "__main__":
    app.run(port=5060)
