#!/usr/bin/env python3
from flask import Flask, jsonify, request
import sqlite3, pathlib, time

app = Flask(__name__)

DB_INV = pathlib.Path.home() / "SHMRY/marketplace/shmry_business.db"
def find_invoice_db():
    candidates = [
        pathlib.Path.home() / "shmry_core/superapp/invoices.db",
        pathlib.Path.home() / "SHMRY/shmry_core/superapp/invoices.db",
        pathlib.Path.home() / "SHMRY/marketplace/invoices.db",
    ]
    for c in candidates:
        if c.exists():
            return c
    return candidates[0]

DB_PAY = pathlib.Path.home() / "shmry_core/superapp/invoices.db"

def qdict(row, cols):
    return dict(zip(cols, row)) if row else {}

@app.route("/health")
def health():
    return jsonify({"status":"healthy","service":"shmry-analytics-fulfillment","version":"v1"})

@app.route("/api/analytics/summary")
def analytics_summary():
    con = sqlite3.connect(DB_INV)
    try:
        inv = con.execute(
            "SELECT COUNT(*) AS sku_count, COALESCE(SUM(qty*price_pkr),0) AS value_pkr FROM rangoons_inventory"
        ).fetchone()
        low = con.execute(
            "SELECT sku,name,qty,price_pkr,city FROM rangoons_inventory ORDER BY qty ASC LIMIT 5"
        ).fetchall()
        leads = con.execute("SELECT COUNT(*) AS total_leads FROM whatsapp_leads").fetchone()
        return jsonify({
            "status":"ok",
            "inventory_value":{"sku_count":inv[0],"value_pkr":inv[1]},
            "low_stock":[
                {"sku":r[0],"name":r[1],"qty":r[2],"price_pkr":r[3],"city":r[4]} for r in low
            ],
            "lead_count":{"total_leads":leads[0]}
        })
    finally:
        con.close()

@app.route("/api/fulfillment/process/<invoice_id>", methods=["POST"])
def fulfillment(invoice_id):
    pay = sqlite3.connect(DB_PAY)
    invdb = sqlite3.connect(DB_INV)
    try:
        row = pay.execute(
            "SELECT service_code,status FROM invoices WHERE id=?",
            (invoice_id,)
        ).fetchone()

        if not row:
            return jsonify({"ok":False,"reason":"invoice_not_found"})

        sku, status = row
        if status != "paid":
            return jsonify({"ok":False,"reason":"invoice_not_paid","status":status,"sku":sku})

        cur = invdb.execute(
            "UPDATE rangoons_inventory SET qty=CASE WHEN qty>0 THEN qty-1 ELSE qty END, updated_at=? WHERE sku=?",
            (int(time.time()), sku)
        )
        invdb.commit()

        return jsonify({
            "ok": cur.rowcount > 0,
            "invoice_id": invoice_id,
            "sku": sku,
            "action": "inventory_decremented" if cur.rowcount else "sku_not_found"
        })
    finally:
        pay.close()
        invdb.close()

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8120)
