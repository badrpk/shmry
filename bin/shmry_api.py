from http.server import BaseHTTPRequestHandler, HTTPServer
import json, sqlite3, datetime
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path.home() / "shmry_cloud_hyperscale"
DB = ROOT / "vault/shmry_cloud.db"
WEB = ROOT / "web"

STATIC_IP = "0.0.0.0"
PORT = 8080

def db():
    return sqlite3.connect(DB)

class SHMRYHandler(BaseHTTPRequestHandler):
    def _json(self, data, code=200):
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(json.dumps(data, indent=2).encode())

    def _html(self):
        index = WEB / "index.html"
        self.send_response(200)
        self.send_header("Content-Type", "text/html")
        self.end_headers()
        self.wfile.write(index.read_bytes())

    def do_GET(self):
        path = urlparse(self.path).path

        if path == "/":
            return self._html()

        if path == "/api/health":
            return self._json({
                "platform": "SHMRY Sovereign Cloud",
                "status": "ONLINE",
                "region": "Islamabad-A",
                "time": datetime.datetime.utcnow().isoformat() + "Z"
            })

        if path == "/api/customers":
            con = db()
            rows = con.execute("SELECT id, name, tier FROM customers").fetchall()
            con.close()
            return self._json([
                {"id": r[0], "name": r[1], "tier": r[2]} for r in rows
            ])

        if path == "/api/instances":
            con = db()
            rows = con.execute("""
                SELECT i.id, i.service, i.status, c.name
                FROM instances i
                JOIN customers c ON i.customer_id = c.id
            """).fetchall()
            con.close()
            return self._json([
                {"id": r[0], "service": r[1], "status": r[2], "customer": r[3]} for r in rows
            ])

        if path == "/api/dashboard":
            con = db()
            rows = con.execute("""
                SELECT c.name, COUNT(DISTINCT i.id), COALESCE(SUM(t.bytes),0)/1048576.0
                FROM customers c
                LEFT JOIN instances i ON c.id = i.customer_id
                LEFT JOIN telemetry t ON i.service = t.service
                GROUP BY c.name
            """).fetchall()
            con.close()
            return self._json([
                {"customer": r[0], "instances": r[1], "data_mb": round(r[2], 2)} for r in rows
            ])

        return self._json({"error": "not found"}, 404)

    def do_OPTIONS(self):
        self.send_response(204)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET,POST,OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type,Authorization")
        self.end_headers()

print(f"🚀 SHMRY API + Web Portal running on http://{STATIC_IP}:{PORT}")
HTTPServer((STATIC_IP, PORT), SHMRYHandler).serve_forever()
