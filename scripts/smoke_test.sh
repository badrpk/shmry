#!/usr/bin/env bash
set -euo pipefail
bash install.sh
bash examples/demo_safe_agent.sh
echo "Smoke test passed."
