# SHMRY Runbook

## Health Check
`./scripts/healthcheck.sh`

## Maintenance
- **Pulse:** `curl -s http://localhost:5000/pulse`
- **Audit:** `tail -f logs/shmry_intelligence.log`
- **Backup:** `cp vault/shmry_cloud.db backups/shmry_$(date +%Y%m%d).db`

## Response
1. `systemctl --user status shmry-intelligence`
2. `find tenants -name instance.json -exec jq empty {} \;`
