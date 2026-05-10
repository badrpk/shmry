import secrets
import sqlite3
from pathlib import Path

DB = Path.home() / "shmry_cloud_hyperscale/vault/shmry_cloud.db"

def rotate_key(customer_name):
    new_key = f"nifdu_sk_{secrets.token_hex(16)}"
    conn = sqlite3.connect(DB)
    # Ensure a 'keys' table exists
    conn.execute("CREATE TABLE IF NOT EXISTS iam_keys (customer TEXT PRIMARY KEY, access_key TEXT)")
    conn.execute("INSERT OR REPLACE INTO iam_keys VALUES (?, ?)", (customer_name, new_key))
    conn.commit()
    conn.close()
    return new_key

if __name__ == "__main__":
    import sys
    cust = sys.argv[1] if len(sys.argv) > 1 else "TechLogix_Global"
    print(f"🔑 New Access Key for {cust}: {rotate_key(cust)}")
