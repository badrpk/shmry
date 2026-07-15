from __future__ import annotations
"""SHMRY observability API — Datadog / Prometheus-class lite surfaces."""
import sys
from pathlib import Path as _P
sys.path.insert(0, str(_P(__file__).resolve().parent))

import time, statistics
from http_util import JsonAPI, serve, uid, iso

HOSTS: dict[str, dict] = {
    "host-1": {"id": "host-1", "name": "edge-khi-01", "tags": ["env:prod", "role:edge"], "status": "up", "last_seen": iso()},
    "host-2": {"id": "host-2", "name": "api-sgp-02", "tags": ["env:prod", "role:api"], "status": "up", "last_seen": iso()},
}
METRICS: list[dict] = []  # {host, name, value, ts, tags}
LOGS: list[dict] = []
ALERTS: list[dict] = [
    {"id": "al1", "name": "High CPU", "query": "avg:cpu{*} > 90", "status": "ok", "notify": ["email:ops@example.com"]},
]
DASHBOARDS: list[dict] = [
    {"id": "db1", "title": "Fleet Overview", "widgets": ["cpu", "mem", "error_rate"]},
]

class H(JsonAPI):
    def do_GET(self):
        path, q = self.parse()
        if path in ("/", "/health"):
            return self._send(200, {"ok": True, "service": "shmry-observability", "version": "2.0.0",
                                    "parity_target": "Datadog / Prometheus+Grafana lite"})
        if path == "/capabilities":
            return self._send(200, {"ok": True, "competitor": "Datadog", "features": [
                "host_inventory", "metrics_ingest", "metrics_query", "logs", "alerts", "dashboards", "tags"
            ]})
        if path == "/api/v1/hosts":
            return self._send(200, {"ok": True, "hosts": list(HOSTS.values())})
        if path == "/api/v1/metrics/query":
            name = (q.get("name") or ["cpu"])[0]
            host = (q.get("host") or [None])[0]
            rows = [m for m in METRICS if m["name"] == name and (not host or m["host"] == host)]
            vals = [m["value"] for m in rows[-50:]]
            return self._send(200, {"ok": True, "name": name, "points": rows[-50:],
                                    "stats": {"count": len(vals), "avg": (sum(vals)/len(vals) if vals else 0),
                                              "max": max(vals) if vals else 0}})
        if path == "/api/v1/logs":
            qtext = ((q.get("q") or [""])[0] or "").lower()
            rows = [l for l in LOGS if not qtext or qtext in l.get("message", "").lower()]
            return self._send(200, {"ok": True, "logs": rows[-100:]})
        if path == "/api/v1/alerts":
            return self._send(200, {"ok": True, "alerts": ALERTS})
        if path == "/api/v1/dashboards":
            return self._send(200, {"ok": True, "dashboards": DASHBOARDS})
        self._send(404, {"ok": False})

    def do_POST(self):
        path, _ = self.parse()
        body = self._read_json()
        if path == "/api/v1/metrics":
            # ingest series
            series = body.get("series") or [body]
            for s in series:
                host = s.get("host") or "host-1"
                if host not in HOSTS:
                    HOSTS[host] = {"id": host, "name": host, "tags": s.get("tags") or [], "status": "up", "last_seen": iso()}
                else:
                    HOSTS[host]["last_seen"] = iso()
                METRICS.append({
                    "host": host, "name": s.get("name") or "cpu", "value": float(s.get("value") or 0),
                    "ts": s.get("ts") or time.time(), "tags": s.get("tags") or [],
                })
                # simple alert evaluation
                if (s.get("name") == "cpu") and float(s.get("value") or 0) > 90:
                    ALERTS[0]["status"] = "alert"
                    ALERTS[0]["last_triggered"] = iso()
            return self._send(202, {"ok": True, "ingested": len(series)})
        if path == "/api/v1/logs":
            LOGS.append({"id": uid("log"), "host": body.get("host") or "host-1",
                         "level": body.get("level") or "info", "message": body.get("message") or "",
                         "at": iso()})
            return self._send(202, {"ok": True})
        if path == "/api/v1/alerts":
            a = {"id": uid("al"), "name": body.get("name") or "Alert", "query": body.get("query") or "",
                 "status": "ok", "notify": body.get("notify") or []}
            ALERTS.append(a)
            return self._send(201, {"ok": True, "alert": a})
        if path == "/api/v1/dashboards":
            d = {"id": uid("db"), "title": body.get("title") or "Dashboard", "widgets": body.get("widgets") or []}
            DASHBOARDS.append(d)
            return self._send(201, {"ok": True, "dashboard": d})
        if path == "/api/v1/hosts":
            hid = body.get("id") or uid("host")
            HOSTS[hid] = {"id": hid, "name": body.get("name") or hid, "tags": body.get("tags") or [],
                          "status": "up", "last_seen": iso()}
            return self._send(201, {"ok": True, "host": HOSTS[hid]})
        self._send(404, {"ok": False})

def main():
    # keep 8787 if health_server uses it — use 8788 for obs or 8787 override
    port = int(__import__("os").environ.get("PORT", "8787"))
    serve(H, port=port, name="SHMRY Observability (Datadog parity)")

if __name__ == "__main__":
    main()
