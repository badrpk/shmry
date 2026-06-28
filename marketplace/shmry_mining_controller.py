import subprocess, time, pathlib, requests, os

XMRIG_API = "http://127.0.0.1:5555/2/summary"
XMRIG = pathlib.Path.home() / "xmrig/build/xmrig"
CONFIG = pathlib.Path.home() / ".xmrig/config.json"
LOG = pathlib.Path.home() / "SHMRY/logs/mining_controller.log"

def _run(cmd):
    return subprocess.run(cmd, shell=True, text=True, capture_output=True, timeout=10)

def xmrig_processes():
    p = _run("pgrep -af 'xmrig' || true")
    lines = []
    for line in p.stdout.splitlines():
        if "pgrep" not in line and "sh -c" not in line:
            lines.append(line)
    return lines

def api_summary():
    try:
        r = requests.get(XMRIG_API, timeout=3)
        if r.status_code == 200:
            return r.json()
    except Exception:
        pass
    return None

def status():
    procs = xmrig_processes()
    api = api_summary()
    return {
        "running": bool(procs),
        "processes": procs,
        "api_online": api is not None,
        "api_summary": api,
        "solar_mode": os.environ.get("SHMRY_SOLAR_MODE", "free_solar_assumed"),
        "controller": "shmry_mining_controller_v2",
        "timestamp": int(time.time())
    }

def start():
    if status()["running"]:
        return {"ok": True, "message": "XMRig already running", "status": status()}
    if not XMRIG.exists():
        return {"ok": False, "error": f"xmrig not found at {XMRIG}", "status": status()}
    LOG.parent.mkdir(parents=True, exist_ok=True)
    _run(f"nohup nice -n 10 {XMRIG} --config={CONFIG} >> {LOG} 2>&1 &")
    time.sleep(2)
    return {"ok": True, "message": "XMRig start requested", "status": status()}

def stop():
    _run("pkill -f '[x]mrig' || true")
    time.sleep(1)
    return {"ok": True, "message": "XMRig stop requested", "status": status()}

def solar_policy():
    return {
        "mode": os.environ.get("SHMRY_SOLAR_MODE", "free_solar_assumed"),
        "rule": "Mine only on solar/free power; future upgrade can connect inverter API.",
        "recommended_next": "enable XMRig HTTP API on 127.0.0.1:5555"
    }
