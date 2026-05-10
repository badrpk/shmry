#!/usr/bin/env bash
set -e
ROOT="$HOME/shmry_cloud_hyperscale"
LATEST="$(ls -t "$ROOT"/backups/shmry_cloud_*.db 2>/dev/null | head -n 1)"

if [ -z "$LATEST" ]; then
  echo "No backup found"
  exit 1
fi

cp "$ROOT/vault/shmry_cloud.db" "$ROOT/vault/shmry_cloud.db.pre_restore_$(date +%Y%m%d_%H%M%S)"
cp "$LATEST" "$ROOT/vault/shmry_cloud.db"
echo "Restored: $LATEST"
