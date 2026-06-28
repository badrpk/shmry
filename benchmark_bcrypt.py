import time
import bcrypt
import json

print("🔬 SHMRY Bcrypt Cost Scaling Benchmark")
print("=" * 60)

test_password = b"shmry_benchmark_2026"
results = []

for cost in range(9, 18):
    start = time.perf_counter()
    hashed = bcrypt.hashpw(test_password, bcrypt.gensalt(rounds=cost))
    duration = time.perf_counter() - start
    
    results.append({"cost": cost, "time_seconds": round(duration, 4)})
    print(f"Cost {cost:2d} → {duration:.4f} seconds")

print("\n📊 Full Results:")
print(json.dumps(results, indent=2))

# Recommendation
best = next((r for r in results if r["time_seconds"] <= 0.5), results[-1])
print(f"\n✅ Recommended cost for your hardware: {best['cost']} (~{best['time_seconds']:.3f}s)")
