#!/bin/bash

pkill -f "gunicorn.*5060" 2>/dev/null || true
pkill -f shmry_marketplace.py 2>/dev/null || true

cd ~/shmry_cloud_hyperscale/marketplace || exit 1

nohup gunicorn \
  -w 2 \
  -b 0.0.0.0:5060 \
  shmry_marketplace:app \
  > marketplace.log 2>&1 &

sleep 3

echo
echo "=== MARKETPLACE STATUS ==="

ss -tulpn | grep 5060 || true

echo
curl -s http://127.0.0.1:5060/ | head
