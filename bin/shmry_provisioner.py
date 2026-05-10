import sqlite3, uuid, time, os, subprocess
from pathlib import Path

DB = Path.home() / "shmry_cloud_hyperscale/vault/shmry_cloud.db"
ROOT = Path.home() / "shmry_cloud_hyperscale"

def provision(customer_id, service_type, plan="starter"):
    inst_id = f"shmry-{uuid.uuid4().hex[:8]}"
    
    # 1. Database Entry
    conn = sqlite3.connect(DB)
    conn.execute("INSERT INTO instances VALUES (?, ?, ?, ?, ?, ?, ?)", 
                 (inst_id, customer_id, service_type, plan, "Islamabad-A", "RUNNING", time.time()))
    
    # 2. Fabric Deployment (Docker Simulation)
    print(f"🐳 Deploying Fabric for {service_type}...")
    try:
        # We use nginx as a placeholder for a 'running service'
        subprocess.run(["docker", "run", "-d", "--name", inst_id, "nginx"], check=True, capture_output=True)
        fabric_status = "DOCKER_ACTIVE"
    except:
        fabric_status = "METADATA_ONLY (No Docker)"

    # 3. Filesystem isolation
    path = ROOT / "tenants" / customer_id / inst_id
    path.mkdir(parents=True, exist_ok=True)
    with open(path / "instance.json", "w") as f:
        import json
        json.dump({"id": inst_id, "fabric": fabric_status, "plan": plan}, f)
    
    conn.commit(); conn.close()
    print(f"✅ Provisioned {inst_id} for {customer_id} ({fabric_status})")

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        provision(sys.argv[1], "compute_pro")
