#!/usr/bin/env bash
set -e
ROOT="$HOME/shmry_cloud_hyperscale"
DB="$ROOT/vault/shmry_cloud.db"

echo "SHMRY Healthcheck"
git -C "$ROOT" status --short
sqlite3 "$DB" "SELECT 'Instances: ' || COUNT(*) FROM instances;"
sqlite3 "$DB" "SELECT 'Services: ' || COUNT(*) FROM services;"
sqlite3 "$DB" "SELECT 'CSS Mastery: ' || value FROM sovereign_metrics WHERE name='css_mastery';"
curl -fsS -H "X-NIFDU-Token: EVOLVE_2026" http://localhost:5000/pulse | jq -c '{status,directive,css_mastery}' || echo "Pulse unavailable"
