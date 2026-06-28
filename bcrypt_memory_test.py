import time
import bcrypt
import psutil
import os

print("Bcrypt Memory Usage Test")
print("="*50)

process = psutil.Process(os.getpid())
initial_mem = process.memory_info().rss / 1024 / 1024

for cost in [12, 13, 14]:
    start = time.time()
    pw = b"testpassword123"
    salt = bcrypt.gensalt(rounds=cost)
    hashed = bcrypt.hashpw(pw, salt)
    duration = time.time() - start
    current_mem = process.memory_info().rss / 1024 / 1024
    print(f"Cost {cost}: {duration:.3f}s | Memory delta: {current_mem - initial_mem:.1f} MB")
