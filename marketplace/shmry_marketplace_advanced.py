#!/usr/bin/env python3
from flask import Flask, jsonify, request
import os, sqlite3, json, time, secrets
from pathlib import Path
from datetime import datetime, timedelta, timezone
from dotenv import load_dotenv
import jwt, argon2

load_dotenv()

app = Flask(__name__)
SECRET = os.getenv("SHMRY_SECRET_KEY", "change-this-production-secret")
DB_PATH = Path.home() / "shmry_cloud_hyperscale/vault/shmry_cloud.db"
ph = argon2.PasswordHasher(time_cost=2, memory_cost=64*1024, parallelism=4)

COMMERCIAL_MODULES = {
    "ai_marketplace": "Customer demand capture, supplier matching, quotations, orders",
    "shmry_cash": "Wallet, ledger, QR payments, merchant settlement",
    "ai_customer_service": "WhatsApp/website sales and support agent",
    "ride_hailing": "Ride requests, driver offers, trip settlement",
    "food_delivery": "Restaurants, menus, orders, delivery tracking",
    "cloud_services": "VPS, database, storage, AI API, hosting subscriptions",
    "ai_agents": "Accounting, legal, procurement, sales, solar, steel agents",
    "steel_b2b": "Scrap, billet, rebar, transport, quality certificates",
    "solar_energy": "Solar quotes, installer matching, energy audits",
    "super_app": "Unified marketplace, wallet, messaging, services, agents"
}

def db():
    c = sqlite3.connect(DB_PATH)
    c.row_factory = sqlite3.Row
    return c

def init_db():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    c = db()
    c.executescript("""
    CREATE TABLE IF NOT EXISTS users(
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      username TEXT UNIQUE,
      password_hash TEXT,
      role TEXT DEFAULT 'admin',
      created_at TEXT
    );
    CREATE TABLE IF NOT EXISTS requests(
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      module TEXT,
      text TEXT,
      parsed TEXT,
      status TEXT DEFAULT 'new',
      created_at TEXT
    );
    CREATE TABLE IF NOT EXISTS suppliers(
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      name TEXT,
      module TEXT,
      city TEXT,
      category TEXT,
      price REAL,
      contact TEXT,
      active INTEGER DEFAULT 1
    );
    CREATE TABLE IF NOT EXISTS quotes(
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      request_id INTEGER,
      supplier_id INTEGER,
      amount REAL,
      status TEXT DEFAULT 'offered',
      created_at TEXT
    );
    CREATE TABLE IF NOT EXISTS wallet_accounts(
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      owner TEXT UNIQUE,
      balance REAL DEFAULT 0,
      created_at TEXT
    );
    CREATE TABLE IF NOT EXISTS wallet_tx(
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      txid TEXT UNIQUE,
      from_owner TEXT,
      to_owner TEXT,
      amount REAL,
      note TEXT,
      created_at TEXT
    );
    """)
    admin = c.execute("SELECT id FROM users WHERE username='admin'").fetchone()
    if not admin:
        c.execute("INSERT INTO users(username,password_hash,role,created_at) VALUES(?,?,?,?)",
                  ("admin", ph.hash("shmry123"), "admin", now()))
    if c.execute("SELECT COUNT(*) n FROM suppliers").fetchone()["n"] == 0:
        seed = [
          ("Islamabad Sugar Supplier","ai_marketplace","Islamabad","sugar",190,"03000000001"),
          ("Rawalpindi Wheat Dealer","ai_marketplace","Rawalpindi","wheat",155,"03000000002"),
          ("Lahore Rice Trader","ai_marketplace","Lahore","rice",320,"03000000003"),
          ("SHMRY Solar Installer","solar_energy","Islamabad","solar",80000,"03000000004"),
          ("Steel Scrap Yard","steel_b2b","Rawalpindi","scrap",150000,"03000000005"),
          ("Cloud VPS Node","cloud_services","Online","vps",2500,"cloud@shmry.local"),
          ("Ride Driver Pool","ride_hailing","Islamabad","ride",1200,"03000000006"),
          ("Food Partner Kitchen","food_delivery","Islamabad","food",900,"03000000007"),
          ("AI Accounting Agent","ai_agents","Online","accounting",5000,"agents@shmry.local"),
          ("Support Bot SaaS","ai_customer_service","Online","support",10000,"support@shmry.local"),
        ]
        c.executemany("INSERT INTO suppliers(name,module,city,category,price,contact) VALUES(?,?,?,?,?,?)", seed)
    c.commit(); c.close()

def now():
    return datetime.now(timezone.utc).isoformat()

def token(username, role):
    payload = {"user_id": username, "role": role, "exp": datetime.now(timezone.utc)+timedelta(hours=24)}
    return jwt.encode(payload, SECRET, algorithm="HS256")

def parse_text(text):
    t = (text or "").lower()
    city = "Islamabad"
    for c in ["islamabad","rawalpindi","lahore","karachi","peshawar","quetta","online"]:
        if c in t: city = c.title()
    item = "general"
    for w in ["sugar","rice","wheat","solar","battery","scrap","rebar","billet","ride","food","vps","database","agent","support"]:
        if w in t: item = w
    qty = 1
    import re
    m = re.search(r"(\d+(?:\.\d+)?)\s*(kg|ton|mw|kw|units?)?", t)
    if m: qty = float(m.group(1))
    return {"city": city, "item": item, "qty": qty}

def match_suppliers(module, parsed):
    c = db()
    rows = c.execute("""
      SELECT * FROM suppliers
      WHERE active=1 AND (module=? OR category=? OR city=?)
      ORDER BY CASE WHEN category=? THEN 0 ELSE 1 END, price ASC
      LIMIT 5
    """, (module, parsed["item"], parsed["city"], parsed["item"])).fetchall()
    c.close()
    return [dict(r) for r in rows]

@app.route("/")
def home():
    return jsonify({"message":"SHMRY Commercial Platform Running","version":"v35-commercial-allinone","modules":list(COMMERCIAL_MODULES)})

@app.route("/health")
@app.route("/api/health")
def health():
    return jsonify({"status":"healthy","version":"v35-commercial-allinone","hash":"argon2id","async":"gevent","modules":len(COMMERCIAL_MODULES)})

@app.route("/modules")
def modules():
    return jsonify(COMMERCIAL_MODULES)

@app.route("/auth/login", methods=["POST"])
def login():
    data = request.get_json() or {}
    u,p = data.get("username"), data.get("password")
    c = db(); row = c.execute("SELECT * FROM users WHERE username=?", (u,)).fetchone(); c.close()
    if row and ph.verify(row["password_hash"], p):
        return jsonify({"status":"success","role":row["role"],"token":token(u,row["role"])})
    return jsonify({"status":"error","message":"Unauthorized"}), 401

@app.route("/wa/inbound", methods=["POST"])
@app.route("/request", methods=["POST"])
def inbound():
    data = request.get_json() or {}
    text = data.get("text","")
    module = data.get("module","ai_marketplace")
    parsed = parse_text(text)
    suppliers = match_suppliers(module, parsed)
    c = db()
    cur = c.execute("INSERT INTO requests(module,text,parsed,status,created_at) VALUES(?,?,?,?,?)",
                    (module,text,json.dumps(parsed),"matched" if suppliers else "new",now()))
    rid = cur.lastrowid
    quotes = []
    for s in suppliers:
        amount = float(s["price"]) * float(parsed["qty"])
        c.execute("INSERT INTO quotes(request_id,supplier_id,amount,created_at) VALUES(?,?,?,?)",
                  (rid,s["id"],amount,now()))
        quotes.append({"supplier":s["name"],"amount":amount,"contact":s["contact"]})
    c.commit(); c.close()
    return jsonify({"status":"received","request_id":rid,"module":module,"parsed":parsed,"quotes":quotes})

@app.route("/orders")
@app.route("/requests")
def requests_list():
    c=db()
    rows=c.execute("SELECT * FROM requests ORDER BY id DESC LIMIT 50").fetchall()
    c.close()
    return jsonify([dict(r) for r in rows])

@app.route("/suppliers", methods=["GET","POST"])
def suppliers():
    c=db()
    if request.method=="POST":
        d=request.get_json() or {}
        c.execute("INSERT INTO suppliers(name,module,city,category,price,contact) VALUES(?,?,?,?,?,?)",
                  (d.get("name"),d.get("module","ai_marketplace"),d.get("city","Islamabad"),d.get("category","general"),float(d.get("price",0)),d.get("contact","")))
        c.commit()
    rows=c.execute("SELECT * FROM suppliers ORDER BY id DESC").fetchall()
    c.close()
    return jsonify([dict(r) for r in rows])

@app.route("/wallet/create", methods=["POST"])
def wallet_create():
    d=request.get_json() or {}; owner=d.get("owner","admin")
    c=db()
    c.execute("INSERT OR IGNORE INTO wallet_accounts(owner,balance,created_at) VALUES(?,?,?)",(owner,0,now()))
    c.commit()
    bal=c.execute("SELECT * FROM wallet_accounts WHERE owner=?",(owner,)).fetchone()
    c.close()
    return jsonify(dict(bal))

@app.route("/wallet/transfer", methods=["POST"])
def wallet_transfer():
    d=request.get_json() or {}
    frm,to,amt=d.get("from"),d.get("to"),float(d.get("amount",0))
    txid=secrets.token_hex(12)
    c=db()
    c.execute("INSERT OR IGNORE INTO wallet_accounts(owner,balance,created_at) VALUES(?,?,?)",(frm,0,now()))
    c.execute("INSERT OR IGNORE INTO wallet_accounts(owner,balance,created_at) VALUES(?,?,?)",(to,0,now()))
    c.execute("UPDATE wallet_accounts SET balance=balance-? WHERE owner=?",(amt,frm))
    c.execute("UPDATE wallet_accounts SET balance=balance+? WHERE owner=?",(amt,to))
    c.execute("INSERT INTO wallet_tx(txid,from_owner,to_owner,amount,note,created_at) VALUES(?,?,?,?,?,?)",
              (txid,frm,to,amt,d.get("note",""),now()))
    c.commit(); c.close()
    return jsonify({"status":"success","txid":txid})

@app.route("/wallet/<owner>")
def wallet(owner):
    c=db()
    acc=c.execute("SELECT * FROM wallet_accounts WHERE owner=?",(owner,)).fetchone()
    tx=c.execute("SELECT * FROM wallet_tx WHERE from_owner=? OR to_owner=? ORDER BY id DESC LIMIT 20",(owner,owner)).fetchall()
    c.close()
    return jsonify({"account":dict(acc) if acc else None,"transactions":[dict(x) for x in tx]})

@app.route("/module/<module>", methods=["POST"])
def module_request(module):
    d=request.get_json() or {}
    d["module"]=module
    with app.test_request_context(json=d):
        return inbound()

init_db()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

# === SHMRY Commercial Compatibility Routes ===
@app.route("/commercial/logistics", methods=["POST"])
def commercial_logistics_alias():
    data = request.get_json(silent=True) or {}
    return jsonify({
        "status": "dispatched",
        "module": "Hyperlocal Delivery Dispatch (SHMRY-Logistics)",
        "order": data.get("id"),
        "tracking": "SHIP-" + secrets.token_hex(4).upper()
    })

@app.route("/commercial/inventory", methods=["POST"])
def commercial_inventory_alias():
    data = request.get_json(silent=True) or {}
    return jsonify({
        "status": "synced",
        "module": "Rangoons Warehouse Management",
        "sku": data.get("sku"),
        "qty": data.get("qty")
    })

@app.route("/commercial/pay", methods=["POST"])
def commercial_pay_alias():
    data = request.get_json(silent=True) or {}
    return jsonify({
        "status": "settled",
        "module": "SHMRY Cash Settlement Engine",
        "amount": data.get("amount"),
        "currency": data.get("currency", "PKR"),
        "transaction_id": "TX-" + secrets.token_hex(5).upper()
    })

@app.route("/commercial/demand", methods=["POST"])
def commercial_demand_alias():
    data = request.get_json(silent=True) or {}
    return jsonify({
        "status": "captured",
        "module": data.get("module", "ai_marketplace"),
        "customer": data.get("customer"),
        "need": data.get("need"),
        "city": data.get("city"),
        "budget": data.get("budget"),
        "order_id": "ORD-" + secrets.token_hex(4).upper()
    })

# === SHMRY Commercial Compatibility Routes ===
@app.route("/commercial/logistics", methods=["POST"])
def commercial_logistics_alias():
    data = request.get_json(silent=True) or {}
    return jsonify({
        "status": "dispatched",
        "module": "Hyperlocal Delivery Dispatch (SHMRY-Logistics)",
        "order": data.get("id"),
        "tracking": "SHIP-" + secrets.token_hex(4).upper()
    })

@app.route("/commercial/inventory", methods=["POST"])
def commercial_inventory_alias():
    data = request.get_json(silent=True) or {}
    return jsonify({
        "status": "synced",
        "module": "Rangoons Warehouse Management",
        "sku": data.get("sku"),
        "qty": data.get("qty")
    })

@app.route("/commercial/pay", methods=["POST"])
def commercial_pay_alias():
    data = request.get_json(silent=True) or {}
    return jsonify({
        "status": "settled",
        "module": "SHMRY Cash Settlement Engine",
        "amount": data.get("amount"),
        "currency": data.get("currency", "PKR"),
        "transaction_id": "TX-" + secrets.token_hex(5).upper()
    })

@app.route("/commercial/demand", methods=["POST"])
def commercial_demand_alias():
    data = request.get_json(silent=True) or {}
    return jsonify({
        "status": "captured",
        "module": data.get("module", "ai_marketplace"),
        "customer": data.get("customer"),
        "need": data.get("need"),
        "city": data.get("city"),
        "budget": data.get("budget"),
        "order_id": "ORD-" + secrets.token_hex(4).upper()
    })

# === SHMRY Commercial Compatibility Routes ===
@app.route("/commercial/logistics", methods=["POST"])
def commercial_logistics_alias():
    data = request.get_json(silent=True) or {}
    return jsonify({
        "status": "dispatched",
        "module": "Hyperlocal Delivery Dispatch (SHMRY-Logistics)",
        "order": data.get("id"),
        "tracking": "SHIP-" + secrets.token_hex(4).upper()
    })

@app.route("/commercial/inventory", methods=["POST"])
def commercial_inventory_alias():
    data = request.get_json(silent=True) or {}
    return jsonify({
        "status": "synced",
        "module": "Rangoons Warehouse Management",
        "sku": data.get("sku"),
        "qty": data.get("qty")
    })

@app.route("/commercial/pay", methods=["POST"])
def commercial_pay_alias():
    data = request.get_json(silent=True) or {}
    return jsonify({
        "status": "settled",
        "module": "SHMRY Cash Settlement Engine",
        "amount": data.get("amount"),
        "currency": data.get("currency", "PKR"),
        "transaction_id": "TX-" + secrets.token_hex(5).upper()
    })

@app.route("/commercial/demand", methods=["POST"])
def commercial_demand_alias():
    data = request.get_json(silent=True) or {}
    return jsonify({
        "status": "captured",
        "module": data.get("module", "ai_marketplace"),
        "customer": data.get("customer"),
        "need": data.get("need"),
        "city": data.get("city"),
        "budget": data.get("budget"),
        "order_id": "ORD-" + secrets.token_hex(4).upper()
    })
