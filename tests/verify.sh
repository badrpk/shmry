#!/usr/bin/env bash
set -euo pipefail
echo "[Test] Running syntax check..."
python3 -m py_compile "$HOME/SHMRY/shmry_harness.py"
[ -f "$HOME/shmry_ai_executor.py" ] && python3 -m py_compile "$HOME/shmry_ai_executor.py" || true
if compgen -G "$HOME/SHMRY/mutation_lab/*.py" >/dev/null; then
  python3 -m py_compile "$HOME"/SHMRY/mutation_lab/*.py
fi
echo "✅ Verification Passed."
