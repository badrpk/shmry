#!/usr/bin/env bash
set -euo pipefail
python3 -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt
mkdir -p "$HOME/.shmry/memory" "$HOME/.shmry/logs"
echo '{"type":"system","status":"initialized"}' > "$HOME/.shmry/memory/registry.jsonl"
echo "Install complete. Run: bash examples/demo_safe_agent.sh"
