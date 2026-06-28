from flask import Flask, request, jsonify
import sqlite3, pathlib, time, secrets

DB = pathlib.Path.home() / "SHMRY/marketplace/nifdu_platform.db"
app = Flask(__name__)

def db():
    con = sqlite3.connect(DB)
    con.row_factory = sqlite3.Row
    return con

def init_db():
    with db() as c:
        c.executescript("""
        CREATE TABLE IF NOT EXISTS users(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            whatsapp TEXT UNIQUE,
            name TEXT,
            created_at INTEGER
        );

        CREATE TABLE IF NOT EXISTS devices(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            device_id TEXT,
            trusted_token TEXT,
            trusted_until INTEGER,
            UNIQUE(user_id, device_id)
        );

        CREATE TABLE IF NOT EXISTS otp_sessions(
            whatsapp TEXT PRIMARY KEY,
            otp TEXT,
            expires_at INTEGER
        );

        CREATE TABLE IF NOT EXISTS merchants(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            shop_name TEXT,
            category TEXT,
            city TEXT,
            created_at INTEGER
        );

        CREATE TABLE IF NOT EXISTS captains(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            vehicle_type TEXT,
            city TEXT,
            created_at INTEGER
        );

        CREATE TABLE IF NOT EXISTS merchant_inventory(
            sku TEXT PRIMARY KEY,
            merchant_id INTEGER,
            name TEXT,
            category TEXT,
            price_pkr REAL,
            qty REAL,
            city TEXT,
            updated_at INTEGER
        );

        CREATE TABLE IF NOT EXISTS captain_inventory(
            sku TEXT PRIMARY KEY,
            captain_id INTEGER,
            source_merchant_sku TEXT,
            name TEXT,
            category TEXT,
            price_pkr REAL,
            qty REAL,
            city TEXT,
            updated_at INTEGER
        );

        CREATE TABLE IF NOT EXISTS orders(
            id TEXT PRIMARY KEY,
            user_id INTEGER,
            service_type TEXT,
            sku TEXT,
            qty REAL,
            status TEXT,
            created_at INTEGER
        );

        CREATE TABLE IF NOT EXISTS rides(
            id TEXT PRIMARY KEY,
            user_id INTEGER,
            pickup TEXT,
            dropoff TEXT,
            status TEXT,
            created_at INTEGER
        );
        """)

        c.execute("INSERT OR IGNORE INTO users(whatsapp,name,created_at) VALUES('03003811243','Admin',?)", (int(time.time()),))
        uid = c.execute("SELECT id FROM users WHERE whatsapp='03003811243'").fetchone()["id"]

        c.execute("INSERT OR IGNORE INTO merchants(id,user_id,shop_name,category,city,created_at) VALUES(1,?,?,?,?,?)",
                  (uid, "Rangoons Merchant Store", "general", "Rawalpindi/Islamabad", int(time.time())))
        c.execute("INSERT OR IGNORE INTO captains(id,user_id,vehicle_type,city,created_at) VALUES(1,?,?,?,?)",
                  (uid, "bike", "Rawalpindi/Islamabad", int(time.time())))

        seed = [
            ("MER-GROCERY-001",1,"Grocery / Daily Items","grocery",1000,100,"Rawalpindi/Islamabad"),
            ("MER-MED-001",1,"Medicine Delivery Item","medicine",500,50,"Rawalpindi/Islamabad"),
            ("MER-STEEL-001",1,"Construction Steel / Rebar","construction",182000,10,"Rawalpindi/Islamabad"),
            ("MER-ELEC-001",1,"Electronics Item","electronics",2500,20,"Rawalpindi/Islamabad"),
            ("MER-FOOD-001",1,"Restaurant Food Item","restaurant",750,40,"Rawalpindi/Islamabad"),
        ]
        for row in seed:
            c.execute("""INSERT OR IGNORE INTO merchant_inventory
            (sku,merchant_id,name,category,price_pkr,qty,city,updated_at)
            VALUES(?,?,?,?,?,?,?,?)""", (*row, int(time.time())))

        cap_seed = [
            ("CAP-HOMEFOOD-001",1,"MER-FOOD-001","Homemade Food by Captain","homemade_food",600,15,"Rawalpindi/Islamabad"),
            ("CAP-SNACK-001",1,"MER-GROCERY-001","Captain Nearby Snacks","captain_items",250,30,"Rawalpindi/Islamabad"),
        ]
        for row in cap_seed:
            c.execute("""INSERT OR IGNORE INTO captain_inventory
            (sku,captain_id,source_merchant_sku,name,category,price_pkr,qty,city,updated_at)
            VALUES(?,?,?,?,?,?,?,?,?)""", (*row, int(time.time())))

init_db()

@app.get("/health")
def health():
    return jsonify({"ok": True, "service": "nifdu-platform", "version": "v1-whatsapp-merchant-captain"})

@app.post("/auth/request_otp")
def request_otp():
    data = request.get_json(force=True)
    whatsapp = data.get("whatsapp","").strip()
    if not whatsapp:
        return jsonify({"ok": False, "reason": "whatsapp_required"}), 400
    otp = "123456"
    with db() as c:
        c.execute("INSERT OR REPLACE INTO otp_sessions(whatsapp,otp,expires_at) VALUES(?,?,?)",
                  (whatsapp, otp, int(time.time()) + 300))
    return jsonify({"ok": True, "whatsapp": whatsapp, "otp_demo": otp})

@app.post("/auth/verify_otp")
def verify_otp():
    data = request.get_json(force=True)
    whatsapp = data.get("whatsapp","").strip()
    otp = data.get("otp","").strip()
    device_id = data.get("device_id","default-device")
    now = int(time.time())
    with db() as c:
        row = c.execute("SELECT otp,expires_at FROM otp_sessions WHERE whatsapp=?", (whatsapp,)).fetchone()
        if not row or row["otp"] != otp or row["expires_at"] < now:
            return jsonify({"ok": False, "reason": "invalid_or_expired_otp"}), 401
        c.execute("INSERT OR IGNORE INTO users(whatsapp,name,created_at) VALUES(?,?,?)", (whatsapp, "", now))
        user = c.execute("SELECT id FROM users WHERE whatsapp=?", (whatsapp,)).fetchone()
        token = secrets.token_hex(24)
        c.execute("""INSERT OR REPLACE INTO devices(user_id,device_id,trusted_token,trusted_until)
                     VALUES(?,?,?,?)""", (user["id"], device_id, token, now + 86400*180))
    return jsonify({"ok": True, "user_id": user["id"], "trusted_token": token})

@app.post("/auth/device_login")
def device_login():
    data = request.get_json(force=True)
    token = data.get("trusted_token","")
    now = int(time.time())
    with db() as c:
        row = c.execute("SELECT user_id FROM devices WHERE trusted_token=? AND trusted_until>?", (token, now)).fetchone()
    if not row:
        return jsonify({"ok": False, "reason": "otp_required"}), 401
    return jsonify({"ok": True, "user_id": row["user_id"], "login": "trusted_device"})

@app.post("/merchant/inventory/upsert")
def merchant_upsert():
    d = request.get_json(force=True)
    with db() as c:
        c.execute("""INSERT OR REPLACE INTO merchant_inventory
        (sku,merchant_id,name,category,price_pkr,qty,city,updated_at)
        VALUES(?,?,?,?,?,?,?,?)""",
        (d["sku"], d.get("merchant_id",1), d["name"], d.get("category","general"),
         float(d.get("price_pkr",0)), float(d.get("qty",0)), d.get("city","Rawalpindi/Islamabad"), int(time.time())))
    return jsonify({"ok": True, "action": "merchant_inventory_updated", "sku": d["sku"]})

@app.post("/captain/inventory/buy_from_merchant")
def captain_buy():
    d = request.get_json(force=True)
    merchant_sku = d["merchant_sku"]
    captain_id = int(d.get("captain_id",1))
    qty = float(d.get("qty",1))
    with db() as c:
        mer = c.execute("SELECT * FROM merchant_inventory WHERE sku=?", (merchant_sku,)).fetchone()
        if not mer:
            return jsonify({"ok": False, "reason": "merchant_sku_not_found"}), 404
        if mer["qty"] < qty:
            return jsonify({"ok": False, "reason": "merchant_stock_low"}), 400
        c.execute("UPDATE merchant_inventory SET qty=qty-?, updated_at=? WHERE sku=?", (qty, int(time.time()), merchant_sku))
        cap_sku = "CAP-" + merchant_sku
        c.execute("""INSERT INTO captain_inventory
        (sku,captain_id,source_merchant_sku,name,category,price_pkr,qty,city,updated_at)
        VALUES(?,?,?,?,?,?,?,?,?)
        ON CONFLICT(sku) DO UPDATE SET qty=qty+excluded.qty, updated_at=excluded.updated_at""",
        (cap_sku, captain_id, merchant_sku, mer["name"], "captain_resale", mer["price_pkr"]*1.10, qty, mer["city"], int(time.time())))
    return jsonify({"ok": True, "action": "captain_inventory_loaded", "captain_sku": cap_sku})

@app.get("/inventory")
def inventory():
    with db() as c:
        merchants = [dict(r) for r in c.execute("SELECT * FROM merchant_inventory ORDER BY category,name").fetchall()]
        captains = [dict(r) for r in c.execute("SELECT * FROM captain_inventory ORDER BY category,name").fetchall()]
    return jsonify({"ok": True, "merchant_inventory": merchants, "captain_inventory": captains})

@app.post("/ai/route")
def ai_route():
    q = request.get_json(force=True).get("query","").lower()
    if any(w in q for w in ["ride","taxi","pickup","drop"]):
        service = "ride_hailing"
    elif any(w in q for w in ["homemade","captain","nearby driver","snack"]):
        service = "captain_marketplace"
    elif any(w in q for w in ["grocery","medicine","electronics","cement","steel","restaurant","construction"]):
        service = "merchant_marketplace"
    else:
        service = "merchant_marketplace"
    return jsonify({"ok": True, "query": q, "service_type": service})

@app.post("/order")
def order():
    d = request.get_json(force=True)
    service = d.get("service_type")
    sku = d.get("sku")
    qty = float(d.get("qty",1))
    order_id = "NIFDU-" + secrets.token_hex(8).upper()
    table = "captain_inventory" if service == "captain_marketplace" else "merchant_inventory"

    if service == "ride_hailing":
        with db() as c:
            c.execute("INSERT INTO rides(id,user_id,pickup,dropoff,status,created_at) VALUES(?,?,?,?,?,?)",
                      (order_id, d.get("user_id",1), d.get("pickup",""), d.get("dropoff",""), "requested", int(time.time())))
        return jsonify({"ok": True, "order_id": order_id, "service_type": service})

    with db() as c:
        row = c.execute(f"SELECT qty FROM {table} WHERE sku=?", (sku,)).fetchone()
        if not row:
            return jsonify({"ok": False, "reason": "sku_not_found"}), 404
        if row["qty"] < qty:
            return jsonify({"ok": False, "reason": "out_of_stock"}), 400
        c.execute(f"UPDATE {table} SET qty=qty-?, updated_at=? WHERE sku=?", (qty, int(time.time()), sku))
        c.execute("INSERT INTO orders(id,user_id,service_type,sku,qty,status,created_at) VALUES(?,?,?,?,?,?,?)",
                  (order_id, d.get("user_id",1), service, sku, qty, "confirmed", int(time.time())))
    return jsonify({"ok": True, "order_id": order_id, "service_type": service, "sku": sku, "qty": qty})

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8130, debug=False)
