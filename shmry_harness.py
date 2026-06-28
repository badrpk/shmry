#!/usr/bin/env python3
import sys, subprocess
from pathlib import Path

HOME = Path.home()
EXEC = HOME / "shmry_ai_executor.py"

def run(cmd, timeout=15):
    try:
        return subprocess.check_output(cmd, shell=True, text=True, stderr=subprocess.STDOUT, timeout=timeout).strip()
    except:
        return "N/A"

def get_status():
    uptime = run("uptime -p")
    ram = run("free -h | awk '/Mem:/ {print $3\" / \"$2}'")
    disk = run("df -h $HOME | tail -1 | awk '{print $3\" / \"$2\" (\"$5\")\"}'")
    py = run("python3 --version")
    return f"""✅ SHMRY Strong Harness Online
Runtime:
- Uptime: {uptime}
- RAM: {ram}
- Disk: {disk}
- Python: {py}"""

def router(query):
    q = query.lower().strip()
    if "scan code" in q:
        return "🧪 SHMRY Code Scan\n" + run("python3 -m py_compile ~/SHMRY/*.py 2>&1 && echo '✅ Syntax OK'")
    if "mining" in q or "solar" in q or "s21" in q:
        try:
            from prod_safe.enhanced_mining_psx import mining_dashboard
            return mining_dashboard()
        except:
            return "⛏️ Mining: " + run("pgrep -f miner && echo 'Active (solar)' || echo 'Inactive'") + "\n6kW + 700Ah"
    if "psx" in q or "luck" in q or "best" in q:
        try:
            from prod_safe.enhanced_mining_psx import psx_quick
            return psx_quick(query)
        except:
            return "PSX: LUCK strong in cement."
    if any(word in q for word in ["mined", "value", "earnings", "pkr", "crypto"]):
        try:
            from prod_safe.crypto_earnings import crypto_value
            return crypto_value(query)
        except:
            return "💰 Mining on free solar. Share pool details for exact PKR value."
    return "OK. Ready for new mutations."

print(get_status())
if len(sys.argv) > 1:
    print(router(" ".join(sys.argv[1:])))
