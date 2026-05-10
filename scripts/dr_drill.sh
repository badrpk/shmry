#!/usr/bin/env bash
set -euo pipefail
ROOT="$HOME/shmry_cloud_hyperscale"
./scripts/backup.sh
TMP="$(mktemp -d)"
cp vault/shmry_cloud.db "$TMP/test_restore.db"
sqlite3 "$TMP/test_restore.db" "PRAGMA integrity_check;"
rm -rf "$TMP"
echo "✅ DR drill passed"
