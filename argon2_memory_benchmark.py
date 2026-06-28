import time
import argon2
import psutil
import os
import json

print("🔬 Argon2id Memory Hardness Test")
print("="*60)

ph = argon2.PasswordHasher(time_cost=2, memory_cost=64*1024, parallelism=4)  # 64 MiB

process = psutil.Process(os.getpid())
initial = process.memory_info().rss / (1024*1024)

for memory_mb in [16, 32, 64, 128]:
    ph = argon2.PasswordHasher(time_cost=2, memory_cost=memory_mb*1024, parallelism=4)
    start = time.time()
    hash = ph.hash("shmry_test_2026")
    duration = time.time() - start
    current = process.memory_info().rss / (1024*1024)
    print(f"Memory {memory_mb:3d} MiB → {duration:.3f}s | RAM delta: {current-initial:.1f} MB")

print("\n✅ Argon2id forces attackers to use large amounts of RAM per guess.")
