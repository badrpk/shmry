import sqlite3
import json
import time
import sys
from pathlib import Path

db_path = Path.home() / "shmry_cloud_hyperscale/vault/shmry_cloud.db"
log_path = Path.home() / "shmry_cloud_hyperscale/logs/commercial_telemetry.log"

with open(log_path, "a") as log:
    log.write(f"=== COMMERCIAL AGGREGATOR ENGINE STARTUP IN 2026 ===\n")

while True:
    try:
        conn = sqlite3.connect(str(db_path))
        cur = conn.cursor()
        
        cur.execute("SELECT slice_id, domain, throughput_ops, status FROM commercial_slices;")
        rows = cur.fetchall()
        
        current_time = time.strftime("%Y-%m-%d %H:%M:%S")
        with open(log_path, "a") as log:
            for row in rows:
                log.write(f"{current_time} 💼 [COMMERCIAL-MONITOR] Slices Active ID: {row[0]} | Throughput: {row[2]} Ops/Sec | State: {row[3]}\n")
        conn.close()
    except Exception as e:
        with open(log_path, "a") as log:
            log.write(f"ERROR reading slice database: {str(e)}\n")
    time.sleep(8)
