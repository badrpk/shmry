#!/bin/bash
set -euo pipefail
LOG_FILE="/home/badrpk/shmry_repair.log"
echo "[$(date)] Starting SHMRY repair sequence..." | tee -a "$LOG_FILE"

# 1. Kill conflicting wallet RPC
WALLET_PID=$(pgrep -f "monero-wallet-rpc" || echo "")
if [ -n "$WALLET_PID" ]; then
    echo "Killing wallet RPC PID $WALLET_PID" | tee -a "$LOG_FILE"
    kill -9 $WALLET_PID 2>/dev/null || true
    sleep 3
fi

# 2. Restart Wallet RPC
echo "Starting Wallet RPC..." | tee -a "$LOG_FILE"
cd /home/badrpk
nohup monero-wallet-rpc --wallet-file /home/badrpk/Monero/wallets/shmry_wallet \
  --password Karachi5846$ --daemon-address 127.0.0.1:18081 \
  --rpc-bind-ip 127.0.0.1 --rpc-bind-port 18082 \
  --disable-rpc-login --trusted-daemon > /home/badrpk/monero-wallet-rpc.log 2>&1 &

# 3. Restart Miner
echo "Starting XMRig..." | tee -a "$LOG_FILE"
cd /home/badrpk/moneroocean
pkill -f xmrig || true
sleep 2
nohup ./xmrig -c config.json > xmrig.log 2>&1 &

echo "[$(date)] Repair completed. Check logs." | tee -a "$LOG_FILE"
