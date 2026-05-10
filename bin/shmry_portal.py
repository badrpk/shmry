import sqlite3
import sys
from pathlib import Path

DB = Path.home() / "shmry_cloud_hyperscale/vault/shmry_cloud.db"

def view_portal(customer_name):
    conn = sqlite3.connect(DB)
    # Find customer ID by name
    customer = conn.execute("SELECT id FROM customers WHERE name=?", (customer_name,)).fetchone()
    
    if not customer:
        print(f"❌ Error: Customer '{customer_name}' not found in SHMRY Registry.")
        return

    cust_id = customer[0]
    
    print(f"\n--- SHMRY CUSTOMER PORTAL: {customer_name} ---")
    print(f"ID: {cust_id} | Region: Islamabad-A | Status: ACTIVE\n")
    
    # Fetch only THIS customer's instances and their data usage
    query = """
        SELECT i.id, i.service, i.plan, COALESCE(SUM(t.bytes), 0) / 1048576.0
        FROM instances i
        LEFT JOIN telemetry t ON i.service = t.service
        WHERE i.customer_id = ?
        GROUP BY i.id
    """
    instances = conn.execute(query, (cust_id,)).fetchall()
    
    print(f"{'INSTANCE ID':<20} | {'SERVICE':<12} | {'PLAN':<10} | {'DATA USED (MB)'}")
    print("-" * 65)
    for inst_id, service, plan, mb in instances:
        print(f"{inst_id:<20} | {service:<12} | {plan:<10} | {mb:.2f} MB")
    
    conn.close()

if __name__ == "__main__":
    target = sys.argv[1] if len(sys.argv) > 1 else "TechLogix_Global"
    view_portal(target)
