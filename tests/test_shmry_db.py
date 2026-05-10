import os
import sqlite3

ROOT = os.path.expanduser("~/shmry_cloud_hyperscale")
DB = os.path.join(ROOT, "vault", "shmry_cloud.db")

def test_db_exists():
    assert os.path.exists(DB)

def test_instances_services_present():
    con = sqlite3.connect(DB)
    cur = con.cursor()
    cur.execute("SELECT COUNT(*) FROM instances")
    instances = cur.fetchone()[0]
    cur.execute("SELECT COUNT(*) FROM services")
    services = cur.fetchone()[0]
    con.close()
    assert instances >= 1
    assert services >= 1

def test_css_mastery_present():
    con = sqlite3.connect(DB)
    cur = con.cursor()
    cur.execute("SELECT value FROM sovereign_metrics WHERE name='css_mastery'")
    row = cur.fetchone()
    con.close()
    assert row is not None
    assert float(row[0]) >= 0
