#!/usr/bin/env bash
set -euo pipefail

pkill -f gunicorn 2>/dev/null || true
sleep 2

cd ~/SHMRY/marketplace

nohup ~/shmry_venv/bin/gunicorn \
  --chdir ~/SHMRY/marketplace \
  -k gevent \
  --workers 3 \
  --bind 0.0.0.0:5000 \
  shmry_marketplace_commercial:app > ~/SHMRY/commercial_gunicorn.log 2>&1 &

echo "✅ Restarted with proper chdir"
sleep 2
curl -s http://127.0.0.1:5000/status | python3 -m json.tool || echo "Still not up, check log"
tail -n 30 ~/SHMRY/commercial_gunicorn.log
