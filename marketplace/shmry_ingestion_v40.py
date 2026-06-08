import sqlite3, requests, time
from pathlib import Path

DB = str(Path.home() / "shmry_cloud_hyperscale/vault/shmry_cloud.db")
GATEWAY = "http://127.0.0.1:5060/api/adaptive_ontology"

con = sqlite3.connect(DB, timeout=10)
con.execute("""CREATE TABLE IF NOT EXISTS inventory_enrichment(
 sku TEXT PRIMARY KEY,
 reasoning TEXT,
 status TEXT,
 last_updated INTEGER
)""")
con.commit()

items = con.execute("""
SELECT sku, name FROM rangoons_inventory
WHERE COALESCE(status,'new')='new'
LIMIT 10
""").fetchall()

print("ITEMS_FOUND=", len(items))

for sku, name in items:
    print(f"🔄 Reasoning: {sku} | {name}")
    try:
        r = requests.post(GATEWAY, json={"message": f"Procurement analysis for: {name}"}, timeout=60)
        reply = r.json().get("reply", r.text[:500])
        status = "done"
    except Exception as e:
        reply = "FAILED: " + str(e)
        status = "failed"

    con.execute("""
    INSERT OR REPLACE INTO inventory_enrichment
    (sku, reasoning, status, last_updated)
    VALUES (?, ?, ?, ?)
    """, (sku, reply, status, int(time.time())))

    if status == "done":
        con.execute("UPDATE rangoons_inventory SET status='enriched' WHERE sku=?", (sku,))

    con.commit()
    print("✅", sku, status, reply[:120])

con.close()
