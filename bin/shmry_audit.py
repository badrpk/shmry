import sqlite3
from pathlib import Path

DB = Path.home() / "shmry_cloud_hyperscale/vault/shmry_cloud.db"

def run_audit():
    conn = sqlite3.connect(DB)
    print("==========================================")
    print("   SHMRY SOVEREIGN CLOUD - FINAL AUDIT    ")
    print("==========================================")
    
    # 1. Revenue (COALESCE handles the None/Null case)
    rev_query = conn.execute("SELECT COALESCE(SUM(amount), 0) FROM invoices WHERE status='PAID'").fetchone()[0]
    print(f"💰 TOTAL REVENUE: ${rev_query:,.2f}")
    
    # 2. Infrastructure
    count = conn.execute("SELECT COUNT(*) FROM instances WHERE status='RUNNING'").fetchone()[0]
    regions = conn.execute("SELECT region, COUNT(*) FROM instances GROUP BY region").fetchall()
    print(f"🏗️  ACTIVE INSTANCES: {count}")
    for r, c in regions:
        print(f"   - {r}: {c} instances")
        
    # 3. Bandwidth
    bandwidth = conn.execute("SELECT service, COALESCE(SUM(bytes), 0) / 1048576.0 FROM telemetry GROUP BY service").fetchall()
    print(f"\n📡 NETWORK TELEMETRY (MB):")
    for s, mb in bandwidth:
        print(f"   - {s:12}: {mb:.2f} MB")
        
    print("==========================================")
    print("STATUS: SOVEREIGN & SECURE | MAY 2026")
    conn.close()

if __name__ == "__main__":
    run_audit()
