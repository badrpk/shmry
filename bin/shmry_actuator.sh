#!/bin/bash
ENGINE="$HOME/shmry_cloud_hyperscale/bin/perception_buffer"
GUARD_STREAK=0

while true; do
    PULSE=$($ENGINE HEALTH_CHECK)
    STATUS=$(echo $PULSE | jq -r '.status')
    
    case "$STATUS" in
        "AGGRESSIVE_GROWTH")
            GUARD_STREAK=0
            pkill -CONT -f shmry_intelligence_evolver.py
            echo "✅ [ACTUATOR] Volatility Normal. Intelligence Resumed."
            tar --warning=no-file-changed -czf ~/shmry_cloud_hyperscale/vault/backups/state_$(date +%s).tar.gz ~/shmry_cloud_hyperscale/logs/*.log
            ;;
        "VOLATILITY_GUARD")
            pkill -STOP -f shmry_intelligence_evolver.py
            echo "⚠️ [ACTUATOR] Volatility Critical. Intelligence Paused."

            ((GUARD_STREAK++))
            if [ $GUARD_STREAK -ge 10 ]; then
                echo "🚨 [WATCHDOG] Force-cooling system."
                sqlite3 ~/shmry_cloud_hyperscale/vault/shmry_cloud.db "UPDATE sovereign_metrics SET value = 0.10 WHERE name = 'market_volatility';"
                GUARD_STREAK=0
            fi
            ;;
        *)
            GUARD_STREAK=0
            ;;
    esac
    sleep 60
done
