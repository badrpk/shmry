#!/usr/bin/env bash
set -euo pipefail
DB="$HOME/shmry_cloud_hyperscale/vault/shmry_cloud.db"
SERVICES="$(sqlite3 "$DB" 'SELECT COUNT(*) FROM services;')"
INSTANCES="$(sqlite3 "$DB" 'SELECT COUNT(*) FROM instances;')"
TOTAL="$(awk "BEGIN {print ($SERVICES * 0.01) + ($INSTANCES * 0.02)}")"
sqlite3 "$DB" "INSERT INTO billing_ledger(service,units,unit_price,total) VALUES('shmry_runtime',$((SERVICES+INSTANCES)),0.01,$TOTAL);"
echo "metered total: $TOTAL"
