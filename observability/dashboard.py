#!/usr/bin/env python3
import html
import os
import sqlite3
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

ROOT = os.environ.get("SHMRY_ROOT", "/app")
DB = os.path.join(ROOT, "vault", "shmry_cloud.db")
LOG = os.path.join(ROOT, "logs", "shmry_intelligence.log")

def query(sql, fallback="unknown"):
    try:
        con = sqlite3.connect(DB)
        cur = con.cursor()
        cur.execute(sql)
        row = cur.fetchone()
        con.close()
        return row[0] if row else fallback
    except Exception as e:
        return f"error: {e}"

def recent_logs():
    try:
        if not os.path.exists(LOG):
            return "No log file found."
        with open(LOG, "r", encoding="utf-8", errors="ignore") as f:
            return "".join(f.readlines()[-30:])
    except Exception as e:
        return f"error reading logs: {e}"

class Handler(BaseHTTPRequestHandler):
    def send_text(self, code, body, content_type="text/plain"):
        body = body.encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        instances = query("SELECT COUNT(*) FROM instances")
        services = query("SELECT COUNT(*) FROM services")
        mastery = query("SELECT value FROM sovereign_metrics WHERE name='css_mastery'")
        context = query("SELECT value FROM sovereign_metrics WHERE name='active_context'")

        if self.path == "/healthz":
            self.send_text(200, "ok\n")
            return

        if self.path == "/pulse":
            self.send_text(
                200,
                f'{{"status":"DASHBOARD_ONLINE","instances":{instances},"services":{services},"css_mastery":"{mastery}"}}\n',
                "application/json",
            )
            return

        page = f"""
<!doctype html>
<html>
<head><title>SHMRY Observatory</title></head>
<body style="font-family:system-ui;background:#0b1020;color:#eef;padding:40px">
<h1>SHMRY Observatory</h1>
<p><b>Instances:</b> {html.escape(str(instances))}</p>
<p><b>Services:</b> {html.escape(str(services))}</p>
<p><b>CSS Mastery:</b> {html.escape(str(mastery))}</p>
<p><b>Active Context:</b> {html.escape(str(context))}</p>
<h2>Recent Intelligence Log</h2>
<pre>{html.escape(recent_logs())}</pre>
</body>
</html>
"""
        self.send_text(200, page, "text/html")

ThreadingHTTPServer(("0.0.0.0", 8088), Handler).serve_forever()
