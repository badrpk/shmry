#!/usr/bin/env bash
BASE="$HOME/shmry_cloud_hyperscale"
BIN="$HOME/SHMRY/bin"
LOG="$BASE/logs/watchdog.log"
export NIFDU_TOKEN=EVOLVE_2026
export BUSINESS_BRAIN_URL=http://127.0.0.1:5055

mkdir -p "$BASE/logs"

pgrep -f shmry_evolution_daemon.py >/dev/null || nohup python3 "$BIN/shmry_evolution_daemon.py" >> "$BASE/logs/evolution.log" 2>&1 &
pgrep -f shmry_business_brain.py >/dev/null || nohup python3 "$BASE/business_brain/shmry_business_brain.py" >> "$BASE/logs/business_brain.log" 2>&1 &
pgrep -f "gunicorn.*nifdu_api_www" >/dev/null || (cd "$BIN" && nohup gunicorn -w 2 -b 0.0.0.0:5000 nifdu_api_www:app >> "$BASE/logs/api.log" 2>&1 &)

echo "$(date '+%F %T') watchdog checked" >> "$LOG"
