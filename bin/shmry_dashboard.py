import sqlite3
from pathlib import Path

DB = Path.home() / "shmry_cloud_hyperscale/vault/shmry_cloud.db"

def generate_hq_report():
    conn = sqlite3.connect(DB)
    print("=== SHMRY HYPERSCALE COMMAND CENTER ===")
    
    # Instance Distribution
    rows = conn.execute("""
        SELECT c.name, COUNT(i.id), SUM(t.bytes) / 1048576.0
        FROM customers c
        JOIN instances i ON c.id = i.customer_id
        LEFT JOIN telemetry t ON i.service = t.service
        GROUP BY c.name
    """).fetchall()

    print(f"{'CUSTOMER':<25} | {'INSTANCES':<10} | {'DATA (MB)'}")
    print("-" * 50)
    for name, count, mb in rows:
        mb_val = mb if mb else 0
        print(f"{name:<25} | {count:<10} | {mb_val:.2f} MB")
    
    conn.close()

if __name__ == "__main__":
    generate_hq_report()
