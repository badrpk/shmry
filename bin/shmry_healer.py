import json
import sqlite3
import time
from pathlib import Path

DB = Path.home() / "shmry_cloud_hyperscale/vault/shmry_cloud.db"
ROOT = Path.home() / "shmry_cloud_hyperscale"
LOG = ROOT / "logs/healer.jsonl"

def log(event):
    LOG.parent.mkdir(parents=True, exist_ok=True)
    with LOG.open("a") as f:
        f.write(json.dumps(event) + "\n")

def heal():
    conn = sqlite3.connect(DB)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id, customer_id, service, plan, region, status, created_at
        FROM instances
        WHERE status='RUNNING'
    """)

    healed = 0

    for inst_id, customer_id, service, plan, region, status, created_at in cursor.fetchall():
        path = ROOT / "tenants" / customer_id / inst_id / "instance.json"

        if not path.exists():
            path.parent.mkdir(parents=True, exist_ok=True)
            metadata = {
                "id": inst_id,
                "customer_id": customer_id,
                "service": service,
                "plan": plan,
                "region": region,
                "status": status,
                "isolation": "tenant-directory",
                "created_at": created_at,
                "healed_at": time.time(),
                "healed_by": "shmry_healer"
            }
            path.write_text(json.dumps(metadata, indent=2))
            healed += 1
            log({
                "ts": time.time(),
                "event": "INSTANCE_HEALED",
                "instance_id": inst_id,
                "customer_id": customer_id,
                "service": service
            })
            print(f"🛠️ healed {service}: {inst_id}")

    conn.close()

    if healed == 0:
        print("✅ no healing required")
    else:
        print(f"✅ healing complete: {healed} instance(s) restored")

if __name__ == "__main__":
    heal()
