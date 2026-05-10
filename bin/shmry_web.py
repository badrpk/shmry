from flask import Flask, request, render_template_string, jsonify
import sqlite3, uuid
from pathlib import Path

app = Flask(__name__)
ROOT = Path.home() / "shmry_cloud_hyperscale"
DB = ROOT / "vault/shmry_cloud.db"

HTML = """
<!doctype html>
<html>
<head>
<title>SHMRY Sovereign Portal</title>
<style>
body{background:#101525;color:#e9f6ff;font-family:Arial;padding:40px}
.card{background:#18213a;padding:22px;border-radius:14px;margin:18px 0;max-width:720px}
input,select,button{padding:10px;margin:6px;border-radius:8px;border:0}
button,input[type=submit]{background:#00d4ff;color:#00111a;font-weight:bold}
pre{background:#050814;color:#7dffb2;padding:18px;border-radius:12px;overflow:auto}
</style>
</head>
<body>
<h1>SHMRY Sovereign Cloud</h1>
<p>User Portal + API Gateway</p>

<div class="card">
<h2>Create Sovereign Account</h2>
<form action="/register" method="post">
<input name="name" placeholder="Customer name" required>
<select name="tier">
<option value="starter">Starter - $99</option>
<option value="business">Business - $499</option>
</select>
<input type="submit" value="Initialize Identity">
</form>
</div>

<div class="card">
<h2>API Console</h2>
<button onclick="load('/api/health')">Health</button>
<button onclick="load('/api/customers')">Customers</button>
<button onclick="load('/api/instances')">Instances</button>
<button onclick="load('/api/dashboard')">Dashboard</button>
<pre id="out">Ready.</pre>
</div>

<script>
async function load(path){
  let r = await fetch(path);
  let j = await r.json();
  document.getElementById("out").textContent = JSON.stringify(j,null,2);
}
</script>
</body>
</html>
"""

def con():
    return sqlite3.connect(DB)

def ensure_tables():
    c = con()
    c.execute("""CREATE TABLE IF NOT EXISTS customers(
        id TEXT PRIMARY KEY,
        name TEXT UNIQUE,
        tier TEXT
    )""")
    c.execute("""CREATE TABLE IF NOT EXISTS instances(
        id TEXT PRIMARY KEY,
        customer_id TEXT,
        service TEXT,
        status TEXT
    )""")
    c.execute("""CREATE TABLE IF NOT EXISTS telemetry(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        service TEXT,
        bytes INTEGER
    )""")
    c.commit()
    c.close()

@app.route("/")
def index():
    ensure_tables()
    return render_template_string(HTML)

@app.route("/register", methods=["POST"])
def register():
    ensure_tables()
    name = request.form.get("name", "").strip()
    tier = request.form.get("tier", "starter")

    if not name:
        return jsonify({"error": "name required"}), 400

    cust_id = "cust-" + uuid.uuid4().hex[:8]
    inst_id = "shmry-" + uuid.uuid4().hex[:8]

    c = con()
    try:
        c.execute("INSERT INTO customers(id,name,tier) VALUES(?,?,?)", (cust_id, name, tier))
        c.execute("INSERT INTO instances(id,customer_id,service,status) VALUES(?,?,?,?)",
                  (inst_id, cust_id, "compute_web", "HEALTHY"))
        c.commit()
    except sqlite3.IntegrityError:
        c.close()
        return jsonify({"error": "customer already exists"}), 409

    c.close()
    return jsonify({
        "status": "IDENTITY_PROVISIONED",
        "customer_id": cust_id,
        "instance_id": inst_id,
        "message": f"Welcome to SHMRY, {name}"
    })

@app.route("/api/health")
def health():
    return jsonify({
        "platform": "SHMRY Sovereign Cloud",
        "status": "ONLINE",
        "region": "Islamabad-A"
    })

@app.route("/api/customers")
def customers():
    ensure_tables()
    c = con()
    rows = c.execute("SELECT id,name,tier FROM customers").fetchall()
    c.close()
    return jsonify([{"id":x[0],"name":x[1],"tier":x[2]} for x in rows])

@app.route("/api/instances")
def instances():
    ensure_tables()
    c = con()
    rows = c.execute("""
        SELECT i.id,c.name,i.service,i.status
        FROM instances i LEFT JOIN customers c ON i.customer_id=c.id
    """).fetchall()
    c.close()
    return jsonify([{"id":x[0],"customer":x[1],"service":x[2],"status":x[3]} for x in rows])

@app.route("/api/dashboard")
def dashboard():
    ensure_tables()
    c = con()
    rows = c.execute("""
        SELECT c.name, COUNT(DISTINCT i.id), COALESCE(SUM(t.bytes),0)/1048576.0
        FROM customers c
        LEFT JOIN instances i ON c.id=i.customer_id
        LEFT JOIN telemetry t ON i.service=t.service
        GROUP BY c.name
    """).fetchall()
    c.close()
    return jsonify([{"customer":x[0],"instances":x[1],"data_mb":round(x[2],2)} for x in rows])

if __name__ == "__main__":
    ensure_tables()
    app.run(host="0.0.0.0", port=5000)
