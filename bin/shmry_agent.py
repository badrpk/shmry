import urllib.request
import json
import time
import subprocess
from pathlib import Path

HEALER = Path.home() / "shmry_cloud_hyperscale/bin/shmry_healer.py"
API_URL = "http://localhost:8080/health"

def run_agent():
    print("🤖 SHMRY Autonomic Agent: Engaged.")
    while True:
        try:
            with urllib.request.urlopen(API_URL) as response:
                data = json.loads(response.read().decode())
                # If instances drop below our 'Sovereign 6' baseline
                if data.get("active_instances", 0) < 6:
                    print("⚠️ AGENT: Anomaly detected! Triggering self-healing...")
                    subprocess.run(["python3", str(HEALER)])
                else:
                    print(f"✅ AGENT: System nominal. Uptime 100%. (Instances: {data['active_instances']})")
        except Exception as e:
            print(f"❌ AGENT: Control Plane Unreachable. Error: {e}")
        
        time.sleep(10) # 10-second heartbeat

if __name__ == "__main__":
    run_agent()
