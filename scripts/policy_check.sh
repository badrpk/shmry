#!/usr/bin/env bash
set -euo pipefail
ROOT="$HOME/shmry_cloud_hyperscale"
echo "🔎 Policy check"
test -f "$ROOT/.gitignore"
grep -q "secrets/" "$ROOT/.gitignore" || echo "secrets/" >> "$ROOT/.gitignore"
grep -q "*.env" "$ROOT/.gitignore" || echo "*.env" >> "$ROOT/.gitignore"
grep -q "get-docker.sh" "$ROOT/.gitignore" || echo "get-docker.sh" >> "$ROOT/.gitignore"
echo "✅ Policy baseline enforced"
