#!/usr/bin/env bash
echo "=== SHMRY Status ==="
ps aux | grep -E "gunicorn|flask|shmry|monero|xmrig" | grep -v grep || true
ss -ltnp | grep -E ":5000|:5005|:5060|:8100|:18082|:5555" || true
