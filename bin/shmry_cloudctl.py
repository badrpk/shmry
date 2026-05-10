#!/usr/bin/env python3
import sqlite3, json, uuid, sys, time
from pathlib import Path

ROOT = Path.home() / "shmry_cloud_hyperscale"
DB = ROOT / "vault/shmry_cloud.db"
TENANTS = ROOT / "tenants"
LOG = ROOT / "logs/audit.jsonl"

RATES = {
    "starter": 99,
    "business": 499,
    "enterprise": 2500
}

SERVICES = [
    "compute", "storage", "database", "networking", "security",
    "ai_ml", "analytics", "devops", "productivity", "managed_it"
]

def db():
    con = sqlite3.connect(DB)
    con.execute("""CREATE TABLE IF NOT EXISTS customers(
        id TEXT PRIMARY KEY, name TEXT, tier TEXT, created_at REAL
    )""")
    con.execute("""CREATE TABLE IF NOT EXISTS instances(
        id TEXT PRIMARY KEY, customer_id TEXT, service TEXT, plan TEXT,
        region TEXT, status TEXT, created_at REAL
    )""")
    con.execute("""CREATE TABLE IF NOT EXISTS invoices(
        id TEXT PRIMARY KEY, customer_id TEXT, amount REAL, status TEXT, created_at REAL
    )""")
    con.execute("""CREATE TABLE IF NOT EXISTS sla(
        customer_id TEXT, uptime_target TEXT, support_level TEXT, response_minutes INTEGER
    )""")
    con.commit()
    return con

def audit(event, payload):
    LOG.parent.mkdir(parents=True, exist_ok=True)
    with LOG.open("a") as f:
        f.write(json.dumps({"ts": time.time(), "event": event, "payload": payload}) + "\n")

def onboard(name, tier="enterprise"):
    cid = "cust-" + uuid.uuid4().hex[:8]
    con = db()
    con.execute("INSERT INTO customers VALUES (?, ?, ?, ?)", (cid, name, tier, time.time()))
    con.execute("INSERT INTO sla VALUES (?, ?, ?, ?)", (cid, "99.9%", "priority", 60))
    con.commit()
    (TENANTS / cid).mkdir(parents=True, exist_ok=True)
    audit("CUSTOMER_ONBOARDED", {"customer_id": cid, "name": name, "tier": tier})
    print(f"✅ customer onboarded: {cid}")

def provision(customer_id, service, plan="enterprise", region="Islamabad-A"):
    if service not in SERVICES:
        raise SystemExit(f"❌ unknown service: {service}")
    iid = "shmry-" + uuid.uuid4().hex[:8]
    path = TENANTS / customer_id / iid
    path.mkdir(parents=True, exist_ok=True)
    meta = {
        "id": iid,
        "customer_id": customer_id,
        "service": service,
        "plan": plan,
        "region": region,
        "status": "RUNNING",
        "isolation": "tenant-directory",
        "created_at": time.time()
    }
    (path / "instance.json").write_text(json.dumps(meta, indent=2))
    con = db()
    con.execute("INSERT INTO instances VALUES (?, ?, ?, ?, ?, ?, ?)",
                (iid, customer_id, service, plan, region, "RUNNING", time.time()))
    inv = "inv-" + uuid.uuid4().hex[:8]
    con.execute("INSERT INTO invoices VALUES (?, ?, ?, ?, ?)",
                (inv, customer_id, RATES.get(plan, 0), "DUE", time.time()))
    con.commit()
    audit("INSTANCE_PROVISIONED", meta)
    audit("INVOICE_CREATED", {"invoice_id": inv, "customer_id": customer_id, "amount": RATES.get(plan, 0)})
    print(f"✅ provisioned {service}: {iid}")
    print(f"💳 invoice created: {inv} amount=${RATES.get(plan, 0)}")

def status():
    con = db()
    print("=== SHMRY CLOUD STATUS ===")
    print("customers:", con.execute("SELECT COUNT(*) FROM customers").fetchone()[0])
    print("instances:", con.execute("SELECT COUNT(*) FROM instances").fetchone()[0])
    print("invoices:", con.execute("SELECT COUNT(*) FROM invoices").fetchone()[0])
    print("services:", ", ".join(SERVICES))
    print("mode: commercial_mvp")
    print("truth: local control plane, not real hyperscale fabric")

def audit_print():
    print(LOG.read_text() if LOG.exists() else "no audit log")

cmd = sys.argv[1] if len(sys.argv) > 1 else "status"

if cmd == "onboard":
    onboard(sys.argv[2], sys.argv[3] if len(sys.argv) > 3 else "enterprise")
elif cmd == "provision":
    provision(sys.argv[2], sys.argv[3], sys.argv[4] if len(sys.argv) > 4 else "enterprise")
elif cmd == "status":
    status()
elif cmd == "audit":
    audit_print()
else:
    print("usage:")
    print("  shmry_cloudctl.py onboard CUSTOMER_NAME [tier]")
    print("  shmry_cloudctl.py provision CUSTOMER_ID service [plan]")
    print("  shmry_cloudctl.py status")
    print("  shmry_cloudctl.py audit")
