import sqlite3, time, json
from pathlib import Path

ROOT = Path.home() / "shmry_cloud_hyperscale"
DB = ROOT / "vault/shmry_cloud.db"
LOG = ROOT / "logs/shmry_intelligence.log"

def log(msg):
    LOG.parent.mkdir(parents=True, exist_ok=True)
    line = f"{time.strftime('%Y-%m-%d %H:%M:%S')} {msg}\n"
    LOG.open("a").write(line)
    print(line, end="")

while True:
    try:
        with sqlite3.connect(DB) as c:
            c.row_factory = sqlite3.Row
            services = list(c.execute("SELECT * FROM services"))
            total = len(services)
            missing = [s for s in services if s["endpoint_status"] != "stub-ready"]

            event = {
                "total_services": total,
                "missing_stub_ready": len(missing),
                "action": "audit",
                "policy": "controlled mutation only: log, score, mark metadata; no unsafe self-rewrite"
            }

            c.execute(
                "INSERT INTO shmry_evolution_log(ts,event,detail) VALUES(?,?,?)",
                (int(time.time()), "SHMRY_INTELLIGENCE_AUDIT", json.dumps(event))
            )

            c.execute(
                "UPDATE services SET updated_at=? WHERE endpoint_status='stub-ready'",
                (int(time.time()),)
            )

            metrics = dict(c.execute("SELECT name, value FROM sovereign_metrics"))
            mastery = float(metrics.get("css_mastery", 0) or 0)
            context = metrics.get("active_context", "") or ""

            if any(term in context for term in ["25th Amendment", "CPEC Phase II", "ITTMS", "SEZ"]):
                if mastery < 0.75:
                    new_mastery = min(0.75, mastery + 0.01)
                    c.execute("UPDATE sovereign_metrics SET value=? WHERE name='css_mastery'", (new_mastery,))
                    log(f"✅ Scholarship Mutation: Context integrated. New Mastery: {new_mastery}")

            c.commit()
            log("SHMRY intelligence audit complete: " + json.dumps(event))

    except Exception as e:
        log("SHMRY intelligence error: " + repr(e))

    time.sleep(60)
