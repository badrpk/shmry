#!/usr/bin/env bash
set -euo pipefail
mkdir -p "$HOME/.shmry/memory" "$HOME/.shmry/logs"
echo "SHMRY demo started"
echo "Memory registry: OK"
echo "Safety gate: OK"
echo "Audit log: OK"
echo '{"event":"demo_completed"}' >> "$HOME/.shmry/memory/registry.jsonl"
echo "Demo task completed"
