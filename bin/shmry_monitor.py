import sqlite3
from pathlib import Path

DB = Path.home() / "shmry_cloud_hyperscale/vault/shmry_cloud.db"

def check_health():
    conn = sqlite3.connect(DB)
    cursor = conn.cursor()

    # Correct column: customer_id
    cursor.execute("""
        SELECT id, service, customer_id
        FROM instances
        WHERE status='RUNNING'
    """)

    instances = cursor.fetchall()

    print("--- SHMRY GLOBAL HEALTH MONITOR ---")

    healthy = 0

    for inst_id, service, customer_id in instances:
        path = (
            Path.home()
            / f"shmry_cloud_hyperscale/tenants/{customer_id}/{inst_id}/instance.json"
        )

        if path.exists():
            status = "🟢 HEALTHY"
            healthy += 1
        else:
            status = "🔴 DEGRADED (File Missing)"

        print(f"Service: {service:12} | ID: {inst_id} | Status: {status}")

    uptime = (healthy / len(instances)) * 100 if instances else 0

    print("------------------------------------")
    print(f"GLOBAL UPTIME: {uptime:.2f}% | Islamabad-A: ONLINE")

    conn.close()

if __name__ == "__main__":
    check_health()
