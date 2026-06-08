#!/usr/bin/env python3
import sqlite3, pathlib, json, time, http.server, socketserver, urllib.parse

ROOT = pathlib.Path.home() / "shmry_cloud_hyperscale"
DB = ROOT / "vault/shmry_cloud.db"
LOG = ROOT / "logs/business_brain.log"

def db():
    return sqlite3.connect(DB)

def init():
    con = db()
    cur = con.cursor()

    cur.execute("""CREATE TABLE IF NOT EXISTS inventory(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        item TEXT UNIQUE,
        qty REAL,
        reorder_level REAL,
        cost REAL,
        sale REAL
    )""")

    cur.execute("""CREATE TABLE IF NOT EXISTS leads(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        ts INTEGER,
        customer TEXT,
        phone TEXT,
        need TEXT,
        status TEXT,
        value REAL
    )""")

    cur.execute("""CREATE TABLE IF NOT EXISTS actions(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        ts INTEGER,
        type TEXT,
        message TEXT,
        priority TEXT,
        status TEXT
    )""")

    cur.execute("""CREATE TABLE IF NOT EXISTS daily_profit(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        ts INTEGER,
        revenue REAL,
        cost REAL,
        profit REAL,
        note TEXT
    )""")

    samples = [
        ("Journals", 0, 20, 180, 350),
        ("Socks", 13, 30, 90, 180),
        ("Stationery", 0, 50, 40, 100),
        ("E-bike lead kit", 5, 3, 2500, 6000),
        ("Solar quotation file", 10, 2, 300, 1500),
    ]

    for s in samples:
        cur.execute("""INSERT OR IGNORE INTO inventory
        (item,qty,reorder_level,cost,sale) VALUES(?,?,?,?,?)""", s)

    con.commit()
    con.close()

def log(msg):
    with open(LOG, "a") as f:
        f.write(time.strftime("%Y-%m-%d %H:%M:%S ") + msg + "\n")

def evaluate():
    con = db()
    cur = con.cursor()

    for item, qty, reorder, cost, sale in cur.execute(
        "SELECT item,qty,reorder_level,cost,sale FROM inventory"
    ).fetchall():
        if qty <= reorder:
            msg = f"RESTOCK_REQUIRED: {item} qty={qty} reorder_level={reorder}"
            cur.execute("""INSERT OR IGNORE INTO actions(ts,type,message,priority,status)
            VALUES(?,?,?,?,?)""", (int(time.time()), "RESTOCK", msg, "HIGH", "OPEN"))

    open_leads = cur.execute(
        "SELECT COUNT(*), COALESCE(SUM(value),0) FROM leads WHERE status='OPEN'"
    ).fetchone()

    lead_count, lead_value = open_leads

    if lead_count:
        cur.execute("""INSERT OR IGNORE INTO actions(ts,type,message,priority,status)
        VALUES(?,?,?,?,?)""", (
            int(time.time()),
            "FOLLOWUP",
            f"FOLLOW_UP_LEADS: {lead_count} open leads value={lead_value}",
            "MEDIUM",
            "OPEN"
        ))

    con.commit()
    con.close()

def report():
    con = db()
    cur = con.cursor()

    inventory = cur.execute(
        "SELECT item,qty,reorder_level,cost,sale,(sale-cost) margin FROM inventory ORDER BY margin DESC"
    ).fetchall()

    actions = cur.execute(
        "SELECT type,message,priority,status FROM actions ORDER BY id DESC LIMIT 20"
    ).fetchall()

    leads = cur.execute(
        "SELECT customer,phone,need,status,value FROM leads ORDER BY id DESC LIMIT 20"
    ).fetchall()

    con.close()

    return {
        "system": "SHMRY Business Brain",
        "status": "COMMERCIAL_RUNTIME_ACTIVE",
        "inventory": inventory,
        "actions": actions,
        "leads": leads,
        "directive": "SELL_AS_LOCAL_SME_AUTOPILOT"
    }

class Handler(http.server.BaseHTTPRequestHandler):
    def send(self, obj):
        data = json.dumps(obj, indent=2).encode()
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def do_GET(self):
        path = urllib.parse.urlparse(self.path).path

        if path == "/health":
            self.send({"ok": True, "engine": "SHMRY_BUSINESS_BRAIN"})

        elif path == "/report":
            evaluate()
            self.send(report())

        elif path == "/actions":
            con = db()
            cur = con.cursor()
            rows = cur.execute(
                "SELECT ts,type,message,priority,status FROM actions ORDER BY id DESC LIMIT 50"
            ).fetchall()
            con.close()
            self.send({"actions": rows})

        else:
            self.send({
                "routes": ["/health", "/report", "/actions"],
                "commercial_use": "inventory + WhatsApp leads + profit/autopilot"
            })

    def log_message(self, *args):
        return

if __name__ == "__main__":
    init()
    log("SHMRY Business Brain started")
    evaluate()
    PORT = 5055
    with socketserver.TCPServer(("127.0.0.1", PORT), Handler) as httpd:
        log(f"listening on 127.0.0.1:{PORT}")
        httpd.serve_forever()
