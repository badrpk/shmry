import sqlite3, subprocess, json, time
from pathlib import Path

ROOT = Path.home() / "shmry_cloud_hyperscale"
DB = ROOT / "vault/shmry_cloud.db"
CPP_CORE = ROOT / "bin/perception_buffer"
LOG = ROOT / "logs/evolution.log"

def log(msg):
    LOG.parent.mkdir(parents=True, exist_ok=True)
    line = f"{time.strftime('%Y-%m-%d %H:%M:%S')} {msg}"
    print(line, flush=True)
    LOG.open("a").write(line + "\n")

def decision():
    raw = subprocess.check_output([str(CPP_CORE), "HEALTH_CHECK"], timeout=4)
    return json.loads(raw)

def evolve():
    d = decision()
    integrity = float(d.get("integrity", 1.0))
    directive = d.get("directive", "MAINTAIN")

    with sqlite3.connect(DB) as conn:
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()

        cur.execute("""
        CREATE TABLE IF NOT EXISTS evolution_history(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ts INTEGER,
            service TEXT,
            category TEXT,
            old_status TEXT,
            new_status TEXT,
            integrity REAL,
            directive TEXT,
            event TEXT
        )
        """)

        if directive == "DE-PROVISION_NON_ESSENTIAL":
            rows = cur.execute(
                "SELECT aws_style_service, category, status FROM services WHERE category='specialized' AND status!='OFFLINE' LIMIT 10"
            ).fetchall()
            for r in rows:
                cur.execute("UPDATE services SET status='OFFLINE' WHERE aws_style_service=?", (r["aws_style_service"],))
                cur.execute(
                    "INSERT INTO evolution_history(ts,service,category,old_status,new_status,integrity,directive,event) VALUES(?,?,?,?,?,?,?,?)",
                    (int(time.time()), r["aws_style_service"], r["category"], r["status"], "OFFLINE", integrity, directive, "LOAD_SHED")
                )
            log(f"⚠️ load-shed specialized={len(rows)} integrity={integrity}")
        else:
            optimized_count = cur.execute("SELECT count(*) FROM services WHERE status='OPTIMIZED'").fetchone()[0]
            total_count = cur.execute("SELECT count(*) FROM services").fetchone()[0]
            if total_count and optimized_count / total_count > 0.85:
                log(f"🛡 mutation safety cap active optimized={optimized_count}/{total_count} integrity={integrity}")
                conn.commit()
                return

            row = cur.execute(
                "SELECT aws_style_service, category, status FROM services WHERE status='CATALOG_REGISTERED' ORDER BY aws_style_service LIMIT 1"
            ).fetchone()
            if row:
                cur.execute("UPDATE services SET status='OPTIMIZED' WHERE aws_style_service=?", (row["aws_style_service"],))
                cur.execute(
                    "INSERT INTO evolution_history(ts,service,category,old_status,new_status,integrity,directive,event) VALUES(?,?,?,?,?,?,?,?)",
                    (int(time.time()), row["aws_style_service"], row["category"], row["status"], "OPTIMIZED", integrity, directive, "OPTIMIZE")
                )
                log(f"🧬 optimized={row['aws_style_service']} integrity={integrity}")
            else:
                log(f"✅ all available services already optimized integrity={integrity}")

        conn.commit()

while True:
    try:
        evolve()
    except Exception as e:
        log(f"ERROR {e}")
    time.sleep(10)
