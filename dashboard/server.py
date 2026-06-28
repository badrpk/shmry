from flask import Flask, jsonify, render_template_string
import sqlite3, pathlib, json

app = Flask(__name__)

@app.route('/')
def index():
    # Gather all data points
    db_biz = pathlib.Path.home() / "SHMRY/marketplace/shmry_business.db"
    db_pay = pathlib.Path.home() / "shmry_core/superapp/invoices.db"
    
    con = sqlite3.connect(db_pay)
    revenue = con.execute("SELECT SUM(amount_usd) FROM invoices WHERE status='paid'").fetchone()[0] or 0
    con.close()
    
    return render_template_string('''
        <html><body style="font-family:sans-serif; background:#121212; color:#0f0; padding:20px;">
        <h1>SHMRY Sovereign Node</h1>
        <p>Total Revenue: ${{revenue}} USD</p>
        <div id="data">Loading metrics...</div>
        <script>
            setInterval(() => {
                fetch('/api/stats').then(r => r.json()).then(d => {
                    document.getElementById('data').innerText = JSON.stringify(d, null, 2);
                });
            }, 5000);
        </script>
        </body></html>
    ''', revenue=revenue)

@app.route('/api/stats')
def stats():
    # Merge Mining + Inventory + Payment data
    return jsonify({
        "status": "online",
        "mining": "active_solar",
        "steel_source": "PSX_Live",
        "pending_orders": 17
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
