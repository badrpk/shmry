# SHMRY — competitive parity

**Target:** Datadog / Prometheus+Grafana (lite control plane)

| Feature | API (`scripts/observability_api.py`) |
|---------|--------------------------------------|
| Host inventory | `GET/POST /api/v1/hosts` |
| Metrics ingest + query | `POST /api/v1/metrics`, `GET /api/v1/metrics/query` |
| Logs search | `POST/GET /api/v1/logs` |
| Alerts | `GET/POST /api/v1/alerts` |
| Dashboards | `GET/POST /api/v1/dashboards` |

```bash
python3 scripts/observability_api.py
# http://127.0.0.1:8787/capabilities
```

Existing marketplace/dashboard modules remain for commercial + governance surfaces.
