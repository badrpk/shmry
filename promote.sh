#!/usr/bin/env bash
set -euo pipefail
"$HOME/SHMRY/tests/verify.sh"
mkdir -p "$HOME/SHMRY/prod_safe"
find "$HOME/SHMRY/mutation_lab" -maxdepth 1 -type f -name "*.py" -exec cp {} "$HOME/SHMRY/prod_safe/" \;
echo "✅ Promotion OK."
