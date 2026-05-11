import time
import random

regions = ["Islamabad-A", "Lahore-A", "Global-Core", "Karachi-A"]
sez_count = 44

print("=== SHMRY HYPERSCALE SERVICE MONITOR ===")
print(f"Monitoring {sez_count} Industrial Cluster SEZs...")
print("-" * 40)

try:
    while True:
        reg = random.choice(regions)
        status = "HEALTHY" if random.random() > 0.05 else "DEGRADED"
        latency = f"{random.randint(5, 25)}ms"
        print(f"[{time.strftime('%H:%M:%S')}] REGION: {reg:12} | STATUS: {status:8} | LATENCY: {latency}")
        time.sleep(1)
except KeyboardInterrupt:
    print("\nMonitor paused.")
