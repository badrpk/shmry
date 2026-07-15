from __future__ import annotations
"""SHMRY observability v3 — Datadog gaps + undercut billing."""
import sys, time
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from http_util import JsonAPI, serve, uid, iso
import payments as pay
import auth as authmod

HOSTS = {
    "host-1": {"id": "host-1", "name": "edge-khi-01", "tags": ["env:prod", "role:edge"], "status": "up", "last_seen": iso()},
    "host-2": {"id": "host-2", "name": "api-sgp-02", "tags": ["env:prod", "role:api"], "status": "up", "last_seen": iso()},
}
METRICS, LOGS = [], []
ALERTS = [{"id": "al1", "name": "High CPU", "query": "avg:cpu{*} > 90", "status": "ok", "notify": ["email:ops@example.com"]}]
DASHBOARDS = [{"id": "db1", "title": "Fleet Overview", "widgets": ["cpu", "mem", "error_rate"]}]
APM_TRACES = []
SYNTH = []

class H(JsonAPI):
    def do_GET(self):
        _path_early = (self.path.split("?")[0].rstrip("/") or "/")
        if _path_early.startswith("/auth"):
            hdrs = {k: v for k, v in self.headers.items()}
            code, body = authmod.handle_auth_request("GET", _path_early, {}, hdrs, product="shmry")
            return self._send(code, body)
        path, q = self.parse()
        if path in ("/", "/health"):
            return self._send(200, {"ok": True, "service": "shmry-observability", "version": "3.0.0",
                "gaps_closed": ["apm_traces", "synthetics", "billing_tiers", "stripe", "signup", "login", "otp", "oauth_google", "oauth_facebook"]})
        if path == "/capabilities":
            return self._send(200, {"ok": True, "competitor": "Datadog", "features": [
                "hosts","metrics","logs","alerts","dashboards","apm","synthetics","billing","stripe"]})
        if path == "/pricing": return self._send(200, {"ok": True, **pay.pricing_for("shmry")})
        if path == "/payments/rails": return self._send(200, {"ok": True, "rails": pay.list_rails()})
        if path == "/gap-analysis":
            return self._send(200, {"ok": True, "added": ["APM traces", "synthetics checks", "host billing $4.99 vs ~$15"]})
        if path == "/api/v1/hosts": return self._send(200, {"ok": True, "hosts": list(HOSTS.values())})
        if path == "/api/v1/metrics/query":
            name = (q.get("name") or ["cpu"])[0]
            rows = [m for m in METRICS if m["name"] == name][-50:]
            vals = [m["value"] for m in rows]
            return self._send(200, {"ok": True, "points": rows, "stats": {"avg": (sum(vals)/len(vals) if vals else 0)}})
        if path == "/api/v1/logs":
            qtext = ((q.get("q") or [""])[0] or "").lower()
            rows = [l for l in LOGS if not qtext or qtext in l.get("message","").lower()]
            return self._send(200, {"ok": True, "logs": rows[-100:]})
        if path == "/api/v1/alerts": return self._send(200, {"ok": True, "alerts": ALERTS})
        if path == "/api/v1/dashboards": return self._send(200, {"ok": True, "dashboards": DASHBOARDS})
        if path == "/api/v1/apm/traces": return self._send(200, {"ok": True, "traces": APM_TRACES[-50:]})
        if path == "/api/v1/synthetics": return self._send(200, {"ok": True, "checks": SYNTH})
        self._send(404, {"ok": False})

    def do_POST(self):
        _path_early = (self.path.split("?")[0].rstrip("/") or "/")
        if _path_early.startswith("/auth"):
            hdrs = {k: v for k, v in self.headers.items()}
            body = self._read_json() if hasattr(self, "_read_json") else self._read()
            code, resp = authmod.handle_auth_request("POST", _path_early, body if isinstance(body, dict) else {}, hdrs, product="shmry")
            return self._send(code, resp)
        path, _ = self.parse()
        body = self._read_json()
        if path == "/api/v1/metrics":
            series = body.get("series") or [body]
            for s in series:
                host = s.get("host") or "host-1"
                if host not in HOSTS:
                    HOSTS[host] = {"id": host, "name": host, "tags": s.get("tags") or [], "status": "up", "last_seen": iso()}
                else: HOSTS[host]["last_seen"] = iso()
                METRICS.append({"host": host, "name": s.get("name") or "cpu", "value": float(s.get("value") or 0), "ts": time.time(), "tags": s.get("tags") or []})
                if s.get("name")=="cpu" and float(s.get("value") or 0) > 90:
                    ALERTS[0]["status"] = "alert"; ALERTS[0]["last_triggered"] = iso()
            return self._send(202, {"ok": True, "ingested": len(series)})
        if path == "/api/v1/logs":
            LOGS.append({"id": uid("log"), "host": body.get("host") or "host-1", "level": body.get("level") or "info",
                         "message": body.get("message") or "", "at": iso()})
            return self._send(202, {"ok": True})
        if path == "/api/v1/apm/traces":
            APM_TRACES.append({"id": uid("tr"), "service": body.get("service") or "api", "duration_ms": body.get("duration_ms") or 12,
                               "status": body.get("status") or "ok", "at": iso()})
            return self._send(201, {"ok": True, "trace": APM_TRACES[-1]})
        if path == "/api/v1/synthetics":
            SYNTH.append({"id": uid("syn"), "url": body.get("url") or "https://example.com", "interval_sec": body.get("interval_sec") or 60,
                          "status": "ok", "at": iso()})
            return self._send(201, {"ok": True, "check": SYNTH[-1]})
        if path == "/api/v1/billing/hosts":
            count = int(body.get("hosts") or 1)
            inv = pay.create_invoice("shmry", 4.99 * count, "USD", method=body.get("method") or "stripe",
                                     customer=body.get("customer") or "ops", description=f"{count} host monitors")
            return self._send(201, {"ok": True, "invoice": inv, "note": "$4.99/host vs Datadog ~$15"})
        if path == "/payments/create":
            inv = pay.create_invoice("shmry", float(body.get("amount") or 0), body.get("currency") or "USD",
                method=body.get("method") or "stripe", sku=body.get("sku"), customer=body.get("customer") or "ops")
            return self._send(201, {"ok": True, "invoice": inv})
        if path == "/api/v1/alerts":
            a = {"id": uid("al"), "name": body.get("name") or "Alert", "query": body.get("query") or "", "status": "ok", "notify": body.get("notify") or []}
            ALERTS.append(a); return self._send(201, {"ok": True, "alert": a})
        if path == "/api/v1/dashboards":
            d = {"id": uid("db"), "title": body.get("title") or "Dashboard", "widgets": body.get("widgets") or []}
            DASHBOARDS.append(d); return self._send(201, {"ok": True, "dashboard": d})
        self._send(404, {"ok": False})

def main():
    serve(H, port=int(__import__("os").environ.get("PORT", "8787")), name="SHMRY Observability v3")
if __name__ == "__main__":
    main()
