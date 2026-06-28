from flask import Flask, request, jsonify
import re, sqlite3, datetime, os

app = Flask(__name__)
# Force absolute path based on current script location
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "shmry_business.db")

def init_db():
    conn = sqlite3.connect(DB_PATH)
    conn.execute("CREATE TABLE IF NOT EXISTS margin_logs (id INTEGER PRIMARY KEY AUTOINCREMENT, query TEXT, gross_profit REAL, margin REAL, ts TEXT)")
    conn.commit()
    conn.close()

init_db()



@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "healthy", "service": "shmry_marketplace", "version": "v37"})

    text = data.get("text") or request.form.get("Body") or request.values.get("Body") or ""
    
    # Calculation
    nums = [float(x) for x in re.findall(r'\d+(?:\.\d+)?', text)]
    scrap, rebar, kwh, rate, wastage = (nums + [150000, 230000, 700, 30, 5])[:5]
    
    scrap_waste = scrap * (1 + wastage / 100)
    total_cost = (kwh * rate) + scrap_waste
    gross_profit = rebar - total_cost
    margin = (gross_profit / rebar * 100) if rebar else 0
    
    # Logging using ABSOLUTE path
    conn = sqlite3.connect(DB_PATH)
    conn.execute("INSERT INTO margin_logs (query, gross_profit, margin, ts) VALUES (?, ?, ?, ?)",
                 (text[:300], round(gross_profit, 2), round(margin, 2), datetime.datetime.now().isoformat()))
    conn.commit()
    conn.close()
    
    return jsonify({"status": "success", "margin": round(margin, 2)})

if __name__ == "__main__":
    app.run(port=5000)
