import sqlite3, pathlib

DB_INV = pathlib.Path.home() / "SHMRY/marketplace/shmry_business.db"
DB_PAY = pathlib.Path.home() / "shmry_core/superapp/invoices.db"

def process_fulfillment(invoice_id):
    con_pay = sqlite3.connect(DB_PAY)
    con_inv = sqlite3.connect(DB_INV)
    try:
        # Use service_code as defined in your DB
        inv = con_pay.execute("SELECT service_code, status FROM invoices WHERE id=?", (invoice_id,)).fetchone()
        if not inv: return {"ok": False, "reason": "invoice_not_found"}

        sku, status = inv
        if status != "paid": return {"ok": False, "reason": "not_paid"}

        cur = con_inv.execute("UPDATE rangoons_inventory SET qty = qty - 1 WHERE sku=? AND qty > 0", (sku,))
        if cur.rowcount == 0: return {"ok": False, "reason": "out_of_stock"}
        
        con_inv.commit()
        return {"ok": True}
    finally:
        con_pay.close()
        con_inv.close()


def notify_fulfillment(sku, qty):
    import requests
    payload = {"query": f"Order fulfilled: {sku}, remaining stock {qty}"}
    try:
        requests.post("http://127.0.0.1:5060/api/cognitive_commerce", json=payload, timeout=2)
    except Exception:
        pass
