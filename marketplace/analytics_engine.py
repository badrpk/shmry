import sqlite3, pathlib

DB = pathlib.Path.home() / "SHMRY/marketplace/shmry_business.db"

def summary():
    con = sqlite3.connect(DB)
    con.row_factory = sqlite3.Row
    try:
        inv = con.execute(
            "SELECT COUNT(*) sku_count, COALESCE(SUM(qty*price_pkr),0) value_pkr FROM rangoons_inventory"
        ).fetchone()

        low = con.execute(
            "SELECT sku,name,qty,price_pkr,city FROM rangoons_inventory ORDER BY qty ASC LIMIT 5"
        ).fetchall()

        leads = con.execute(
            "SELECT COUNT(*) total_leads FROM whatsapp_leads"
        ).fetchone()

        return {
            "inventory_value": dict(inv),
            "low_stock": [dict(x) for x in low],
            "lead_count": dict(leads)
        }
    finally:
        con.close()
