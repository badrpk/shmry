import sqlite3
import os
import random
from pathlib import Path

DB = Path.home() / "shmry_cloud_hyperscale/vault/shmry_cloud.db"

def unleash_chaos():
    conn = sqlite3.connect(DB)
    cursor = conn.cursor()
    
    # Pick one random "RUNNING" instance to kill
    cursor.execute("SELECT id, customer_id, service FROM instances WHERE status='RUNNING'")
    instances = cursor.fetchall()
    
    if not instances:
        print("❌ No active instances found. Chaos is bored.")
        return

    target = random.choice(instances)
    inst_id, cust_id, service = target
    
    # Simulate "Hardware Failure" by deleting the instance file
    path = Path.home() / f"shmry_cloud_hyperscale/tenants/{cust_id}/{inst_id}/instance.json"
    if path.exists():
        os.remove(path)
        print(f"🔥 CHAOS: Hardware failure in Islamabad-A! Service {service} ({inst_id}) is GONE.")
    
    conn.close()

if __name__ == "__main__":
    unleash_chaos()
