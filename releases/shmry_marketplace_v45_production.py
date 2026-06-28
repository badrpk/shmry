#!/usr/bin/env python3
from flask import Flask, jsonify, request, abort
import os, secrets, json, sqlite3, jwt
from datetime import datetime, timezone
from pathlib import Path
from functools import wraps
from dotenv import load_dotenv
from pymemcache.client import base

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SHMRY_SECRET_KEY', 'shmry-super-secret-2026-change-this-in-production')

memcache = base.Client(('localhost', 11211))

DB_PATH = Path.home() / "shmry_cloud_hyperscale" / "vault" / "shmry_revenue.db"

def init_db():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.executescript('''
        CREATE TABLE IF NOT EXISTS rfqs (rfq_id TEXT PRIMARY KEY, item TEXT, quantity INTEGER, budget REAL, status TEXT DEFAULT 'open', created_at TEXT);
        CREATE TABLE IF NOT EXISTS bids (bid_id TEXT PRIMARY KEY, rfq_id TEXT, supplier TEXT, amount REAL, delivery_days INTEGER, status TEXT DEFAULT 'pending', created_at TEXT);
        CREATE TABLE IF NOT EXISTS supplier_scores (supplier TEXT PRIMARY KEY, credit_score INTEGER DEFAULT 70, reliability REAL DEFAULT 0.85, ontime_rate REAL DEFAULT 0.9, total_orders INTEGER DEFAULT 0, penalties INTEGER DEFAULT 0);
    ''')
    conn.commit()
    conn.close()

init_db()

def token_required(min_role="user"):
    def decorator(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            auth = request.headers.get('Authorization')
            if not auth or not auth.startswith('Bearer '):
                abort(401)
            try:
                payload = jwt.decode(auth.split(" ")[1], app.config['SECRET_KEY'], algorithms=["HS256"])
                request.current_user = payload
                return f(*args, **kwargs)
            except:
                abort(401)
        return decorated
    return decorator

@app.route('/steel/rfq', methods=['POST'])
@token_required(min_role="user")
def create_rfq():
    data = request.get_json()
    rfq_id = f"RFQ-STEEL-{secrets.token_hex(4).upper()}"
    conn = sqlite3.connect(DB_PATH)
    conn.execute("INSERT INTO rfqs (rfq_id, item, quantity, budget, status) VALUES (?,?,?,?,?)",
                 (rfq_id, data.get("item"), data.get("quantity"), data.get("budget"), "open"))
    conn.commit()
    conn.close()
    return jsonify({"rfq_id": rfq_id, "status": "open"})

@app.route('/diagnostic')
def diagnostic():
    try:
        stats = memcache.stats()
        return jsonify({
            "memcached": "connected",
            "stats": {
                "curr_items": stats.get('curr_items', 0),
                "get_hits": stats.get('get_hits', 0),
                "get_misses": stats.get('get_misses', 0),
                "hit_rate": round(stats.get('get_hits', 0) / max(1, stats.get('cmd_get', 1)) * 100, 2)
            }
        })
    except:
        return jsonify({"memcached": "unavailable"})

@app.route('/status')
def status():
    return jsonify({"status": "healthy", "version": "v45-production"})

if __name__ == '__main__':
    print("🚀 SHMRY Production Kernel")
    app.run(host='0.0.0.0', port=5000, debug=False)
