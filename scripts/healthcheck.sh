#!/usr/bin/env bash
echo "🔍 Performing SHMRY Global Health Audit..."
curl -s -H "X-NIFDU-Token: EVOLVE_2026" http://localhost:5000/pulse | jq .
sqlite3 "$HOME/shmry_cloud_hyperscale/vault/shmry_cloud.db" "SELECT status, count(*) FROM instances GROUP BY status;"
