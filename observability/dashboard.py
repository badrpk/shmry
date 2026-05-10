#!/usr/bin/env python3
import os
import sqlite3
from http.server import BaseHTTPRequestHandler, HTTPServer

ROOT = os.path.expanduser("~/shmry_cloud_hyperscale")
DB = os.path.join(ROOT, "vault", "shmry_cloud.db")
LOG = os.path.join(ROOT, "logs", "shmry_intelligence.log")

def q(sql):
    con = sqlite3.connect(DB)
    cur = con.cursor()
    cur.execute(sql)
    val = cur.fetchone()[0]
    con.close()
    return val

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        logs = ""
        if os.path.exists(LOG):
            logs = "".join(open(LOG, errors="ignore").readlines()[-20:])

        html = f"""
        <html><body style="font-family:system-ui;background:#0b1020;color:#eef;padding:40px">
        <h1>SHMRY Observatory</h1>
        <p><b>Instances:</b> {q("SELECT COUNT(*) FROM instances")}</p>
        <p><b>Services:</b> {q("SELECT COUNT(*) FROM services")}</p>
        <p><b>CSS Mastery:</b> {q("SELECT value FROM sovereign_metrics WHERE name='css_mastery'")}</p>
        <h2>Recent Intelligence Log</h2>
        <pre>{logs}</pre>
        </body></html>
        """
        self.send_response(200)
        self.send_header("Content-Type", "text/html")
        self.end_headers()
        self.wfile.write(html.encode())

HTTPServer(("0.0.0.0", 8088), Handler).serve_forever()
