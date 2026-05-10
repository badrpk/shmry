import sqlite3
import random
import time
from pathlib import Path

DB = Path.home() / "shmry_cloud_hyperscale/vault/shmry_cloud.db"

def simulate_telemetry():
    conn = sqlite3.connect(DB)
    services = ["compute", "storage", "ai_ml", "networking"]
    
    print("📡 SHMRY Telemetry Sensor: ACTIVE")
    try:
        while True:
            service = random.choice(services)
            # Simulate a packet of data (1KB to 5MB)
            bandwidth_bytes = random.randint(1024, 5242880) 
            
            conn.execute("INSERT INTO telemetry (service, bytes, timestamp) VALUES (?, ?, ?)", 
                         (service, bandwidth_bytes, time.time()))
            conn.commit()
            
            # Brief sleep to simulate real-world packet intervals
            time.sleep(2)
    except KeyboardInterrupt:
        print("\n📡 Sensor suspended.")
    finally:
        conn.close()

if __name__ == "__main__":
    simulate_telemetry()
