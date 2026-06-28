import sqlite3, datetime

def calculate_and_log(text, scrap, rebar, kwh, rate, wastage):
    scrap_waste = scrap * (1 + wastage / 100)
    total_cost = (kwh * rate) + scrap_waste
    gross_profit = rebar - total_cost
    margin = (gross_profit / rebar * 100) if rebar else 0
    
    # Log to DB
    try:
        conn = sqlite3.connect("marketplace/shmry_business.db")
        conn.execute("INSERT INTO margin_logs (query, gross_profit, margin, ts) VALUES (?, ?, ?, ?)",
                     (text[:300], round(gross_profit, 2), round(margin, 2), datetime.datetime.now().isoformat()))
        conn.commit()
        conn.close()
    except Exception as e:
        print(f"DB Log Error: {e}")
    return round(margin, 2), round(gross_profit, 2)
