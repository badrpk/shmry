#!/usr/bin/env python3
import os, sqlite3
from http.server import BaseHTTPRequestHandler, HTTPServer

ROOT=os.path.expanduser("~/shmry_cloud_hyperscale")
DB=f"{ROOT}/vault/shmry_cloud.db"

def q(sql, fallback=0):
    try:
        con=sqlite3.connect(DB); cur=con.cursor(); cur.execute(sql)
        val=cur.fetchone()[0]; con.close(); return val
    except Exception:
        return fallback

class H(BaseHTTPRequestHandler):
    def do_GET(self):
        body=f"""# HELP shmry_instances Total SHMRY instances
# TYPE shmry_instances gauge
shmry_instances {q("SELECT COUNT(*) FROM instances")}

# HELP shmry_services Total SHMRY services
# TYPE shmry_services gauge
shmry_services {q("SELECT COUNT(*) FROM services")}

# HELP shmry_css_mastery CSS mastery score
# TYPE shmry_css_mastery gauge
shmry_css_mastery {q("SELECT value FROM sovereign_metrics WHERE name='css_mastery'")}
"""
        self.send_response(200)
        self.send_header("Content-Type","text/plain")
        self.end_headers()
        self.wfile.write(body.encode())

HTTPServer(("0.0.0.0",9090),H).serve_forever()
