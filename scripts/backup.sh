#!/usr/bin/env bash
set -e
ROOT="$HOME/shmry_cloud_hyperscale"
STAMP="$(date +%Y%m%d_%H%M%S)"
mkdir -p "$ROOT/backups"
cp "$ROOT/vault/shmry_cloud.db" "$ROOT/backups/shmry_cloud_$STAMP.db"
git -C "$ROOT" rev-parse HEAD > "$ROOT/backups/git_commit_$STAMP.txt"
echo "Backup created: backups/shmry_cloud_$STAMP.db"
