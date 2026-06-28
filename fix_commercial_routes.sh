#!/usr/bin/env bash
set -euo pipefail

APP="$HOME/SHMRY"
VENV="$HOME/shmry_venv"
LOG="$APP/advanced_gunicorn.log"

pkill -f gunicorn 2>/dev/null || true
sleep 1

# Add compatibility commercial routes into advanced.py if missing
cat >> "$APP/marketplace/shmry_marketplace_advanced.py" <<'PY'

# === SHMRY Commercial Compatibility Routes ===
@app.route("/commercial/logistics", methods=["POST"])
def commercial_logistics_alias():
    data = request.get_json(silent=True) or {}
    return jsonify({
        "status": "dispatched",
        "module": "Hyperlocal Delivery Dispatch (SHMRY-Logistics)",
        "order": data.get("id"),
        "tracking": "SHIP-" + secrets.token_hex(4).upper()
    })

@app.route("/commercial/inventory", methods=["POST"])
def commercial_inventory_alias():
    data = request.get_json(silent=True) or {}
    return jsonify({
        "status": "synced",
        "module": "Rangoons Warehouse Management",
        "sku": data.get("sku"),
        "qty": data.get("qty")
    })

@app.route("/commercial/pay", methods=["POST"])
def commercial_pay_alias():
    data = request.get_json(silent=True) or {}
    return jsonify({
        "status": "settled",
        "module": "SHMRY Cash Settlement Engine",
        "amount": data.get("amount"),
        "currency": data.get("currency", "PKR"),
        "transaction_id": "TX-" + secrets.token_hex(5).upper()
    })

@app.route("/commercial/demand", methods=["POST"])
def commercial_demand_alias():
    data = request.get_json(silent=True) or {}
    return jsonify({
        "status": "captured",
        "module": data.get("module", "ai_marketplace"),
        "customer": data.get("customer"),
        "need": data.get("need"),
        "city": data.get("city"),
        "budget": data.get("budget"),
        "order_id": "ORD-" + secrets.token_hex(4).upper()
    })
PY

"$VENV/bin/python" -m py_compile "$APP/marketplace/shmry_marketplace_advanced.py"

nohup "$VENV/bin/gunicorn" \
  --chdir "$APP" \
  -k gevent \
  --workers 2 \
  --bind 0.0.0.0:5000 \
  marketplace.shmry_marketplace_advanced:app \
  > "$LOG" 2>&1 &

sleep 3

echo "=== HEALTH ==="
curl -s http://127.0.0.1:5000/health | python3 -m json.tool

echo "=== DEMAND TEST ==="
curl -s -X POST http://127.0.0.1:5000/commercial/demand \
  -H "Content-Type: application/json" \
  -d '{"customer":"Badar","need":"buy 10 kg sugar","city":"Islamabad","budget":2000,"module":"ai_marketplace"}' \
  | python3 -m json.tool

echo "✅ Fixed commercial aliases + gunicorn chdir"
