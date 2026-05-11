#!/usr/bin/env python3
import json, time, hashlib, subprocess, os
from pathlib import Path
from datetime import datetime, timezone

HOME = Path.home()
BASE = HOME / "shmry_core"
TOOLS = BASE / "tools"
LOGS = BASE / "logs"
RUNTIME = BASE / "runtime"

OUTBOX = BASE / "whatsapp_outbox.jsonl"
SENT = BASE / "whatsapp_sent.jsonl"
LOG = LOGS / "wa_drain.log"
STATE = RUNTIME / "wa_drain_state.json"

ROUTER = TOOLS / "shmry_wa_router.sh"
OPENCLAW = TOOLS / "openclaw_full_power.sh"

LOGS.mkdir(parents=True, exist_ok=True)
RUNTIME.mkdir(parents=True, exist_ok=True)
OUTBOX.touch(exist_ok=True)
SENT.touch(exist_ok=True)

def now_iso():
    return datetime.now(timezone.utc).isoformat()

def log(msg):
    line = f"[{now_iso()}] {msg}"
    print(line, flush=True)
    with open(LOG, "a", encoding="utf-8") as f:
        f.write(line + "\n")

def load_jsonl(path):
    out = []
    if not path.exists():
        return out
    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                out.append(json.loads(line))
            except Exception:
                continue
    return out

def write_jsonl(path, items):
    tmp = path.with_suffix(path.suffix + ".tmp")
    with open(tmp, "w", encoding="utf-8") as f:
        for obj in items:
            f.write(json.dumps(obj, ensure_ascii=False) + "\n")
    tmp.replace(path)

def sent_count():
    try:
        return sum(1 for _ in open(SENT, "r", encoding="utf-8", errors="ignore"))
    except Exception:
        return 0

def queue_fingerprint(items):
    focus = []
    for x in items:
        st = str(x.get("status", "PENDING")).upper()
        if st in ("PENDING", "FAILED", "RETRY", "ROUTER_PENDING", "HANDOFF"):
            focus.append({
                "to": x.get("to"),
                "text": x.get("text") or x.get("msg"),
                "status": st
            })
    raw = json.dumps(focus, ensure_ascii=False, sort_keys=True)
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()

def load_state():
    if not STATE.exists():
        return {}
    try:
        return json.loads(STATE.read_text(encoding="utf-8", errors="ignore"))
    except Exception:
        return {}

def save_state(st):
    STATE.write_text(json.dumps(st, indent=2), encoding="utf-8")

def normalize_outbox():
    items = load_jsonl(OUTBOX)
    changed = False
    for x in items:
        st = str(x.get("status", "PENDING")).upper()
        if st == "FAILED":
            x["status"] = "PENDING"
            x["retry_ts"] = now_iso()
            changed = True
    if changed:
        write_jsonl(OUTBOX, items)
    return items, changed

def trigger_router():
    if ROUTER.exists():
        ROUTER.chmod(0o755)
        r = subprocess.run(
            [str(ROUTER)],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            timeout=120
        )
        return ("router", r.returncode, (r.stdout or "")[:1500], (r.stderr or "")[:1500])

    if OPENCLAW.exists():
        OPENCLAW.chmod(0o755)
        r = subprocess.run(
            [str(OPENCLAW), "cycle"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            timeout=180
        )
        return ("openclaw", r.returncode, (r.stdout or "")[:1500], (r.stderr or "")[:1500])

    return ("none", 127, "", "No shmry_wa_router.sh or openclaw_full_power.sh found")

def main():
    log("router-bridge outbox drain started")

    while True:
        try:
            items, normalized = normalize_outbox()
            pending = [
                x for x in items
                if str(x.get("status", "PENDING")).upper() in ("PENDING", "FAILED", "RETRY", "ROUTER_PENDING", "HANDOFF")
            ]

            if not pending:
                time.sleep(3)
                continue

            st = load_state()
            fp = queue_fingerprint(items)
            last_fp = st.get("last_fp", "")
            last_ts = float(st.get("last_trigger_epoch", 0))
            now_ts = time.time()

            # Trigger when queue changes or 20s elapsed with pending work
            if fp != last_fp or (now_ts - last_ts) >= 20:
                before = sent_count()
                mode, rc, out, err = trigger_router()
                after = sent_count()

                st["last_fp"] = fp
                st["last_trigger_epoch"] = now_ts
                st["last_mode"] = mode
                st["last_rc"] = rc
                st["last_sent_before"] = before
                st["last_sent_after"] = after
                save_state(st)

                if rc == 0:
                    if after > before:
                        log(f"Triggered {mode}: rc=0 sent_delta={after-before}")
                    else:
                        log(f"Triggered {mode}: rc=0 sent_delta=0 (router ran, no new sent lines detected)")
                else:
                    log(f"Trigger FAILED mode={mode} rc={rc} err={err[:300]!r} out={out[:300]!r}")

            time.sleep(4)

        except KeyboardInterrupt:
            log("Stopped by user")
            break
        except Exception as e:
            log(f"ERROR: {e}")
            time.sleep(5)

if __name__ == "__main__":
    main()
