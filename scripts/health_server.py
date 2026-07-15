#!/usr/bin/env python3
"""Minimal SHMRY health endpoint for public clones."""
from __future__ import annotations
import json
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

class H(BaseHTTPRequestHandler):
    def do_GET(self):  # noqa: N802
        body = {
            "ok": True,
            "service": "shmry",
            "product": "Infrastructure telemetry & governance",
            "version": "1.0.0-public",
            "paths": {
                "core": (ROOT / "core").is_dir(),
                "dashboard": (ROOT / "dashboard").is_dir(),
                "marketplace": (ROOT / "marketplace").is_dir(),
                "modules": (ROOT / "modules").is_dir(),
            },
        }
        data = json.dumps(body, indent=2).encode()
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)
    def log_message(self, *a):
        return

if __name__ == "__main__":
    print("SHMRY health on http://127.0.0.1:8787/health")
    HTTPServer(("127.0.0.1", 8787), H).serve_forever()
