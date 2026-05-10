#!/usr/bin/env python3
import base64, json, hmac, hashlib, time, sys

SECRET = b"shmry_sovereign_secret_2026"

def b64(x):
    return base64.urlsafe_b64encode(x).rstrip(b"=").decode()

payload = {
    "user": sys.argv[1] if len(sys.argv) > 1 else "badrpk",
    "exp": int(time.time()) + 3600
}

header = {"alg": "HS256", "typ": "JWT"}
msg = b64(json.dumps(header).encode()) + "." + b64(json.dumps(payload).encode())
sig = hmac.new(SECRET, msg.encode(), hashlib.sha256).digest()
print(msg + "." + b64(sig))
