from flask import Flask, jsonify, render_template_string
import sqlite3
from pathlib import Path

app = Flask(__name__)
DB = Path.home() / "shmry_cloud_hyperscale/vault/shmry_cloud.db"

# AWS-Style Dashboard Template
HTML_CONSOLE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>NIFDU | Management Console</title>
    <style>
        body { margin: 0; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background: #232f3e; color: white; }
        nav { background: #161c24; padding: 10px 20px; display: flex; justify-content: space-between; align-items: center; border-bottom: 3px solid #ff9900; }
        .sidebar { width: 240px; background: #ffffff; color: #232f3e; height: 100vh; position: fixed; padding: 20px; }
        .main { margin-left: 280px; padding: 40px; background: #f2f3f3; color: #232f3e; min-height: 100vh; }
        .card { background: white; border-radius: 4px; padding: 20px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); margin-bottom: 20px; }
        .badge { background: #0073bb; color: white; padding: 4px 8px; border-radius: 3px; font-size: 12px; }
        .status-up { color: #2eb82e; font-weight: bold; }
        h1, h2 { color: #232f3e; }
    </style>
</head>
<body>
    <nav>
        <div style="font-weight: bold; font-size: 20px;">nifdu<span style="color: #ff9900;">.com</span></div>
        <div>Region: <span class="badge">pk-islamabad-1</span></div>
    </nav>
    <div class="sidebar">
        <h3>Services</h3>
        <ul style="list-style: none; padding: 0;">
            <li style="padding: 10px 0; border-bottom: 1px solid #ddd;"><b>EC2</b> (Sovereign Compute)</li>
            <li style="padding: 10px 0; border-bottom: 1px solid #ddd;"><b>S3</b> (Storage Vault)</li>
            <li style="padding: 10px 0; border-bottom: 1px solid #ddd;"><b>SageMaker</b> (Urdu AI)</li>
            <li style="padding: 10px 0; border-bottom: 1px solid #ddd;"><b>IAM</b> (Sovereign Keys)</li>
        </ul>
    </div>
    <div class="main">
        <h1>Cloud Management Console</h1>
        <div class="card">
            <h2>Service Health</h2>
            <p>Global Infrastructure: <span class="status-up">Operational</span></p>
        </div>
        <div class="card">
            <h2>Active Instances (Islamabad-A)</h2>
            <table style="width: 100%; text-align: left;">
                <tr><th>ID</th><th>Service</th><th>Customer</th><th>Status</th></tr>
                {% for row in instances %}
                <tr>
                    <td><code>{{ row[1] }}</code></td>
                    <td>{{ row[2] }}</td>
                    <td>{{ row[0] }}</td>
                    <td><span class="status-up">RUNNING</span></td>
                </tr>
                {% endfor %}
            </table>
        </div>
    </div>
</body>
</html>
"""

@app.route('/')
def console():
    conn = sqlite3.connect(DB)
    # Pull instance and customer data
    instances = conn.execute("SELECT customer, id, service FROM instances").fetchall()
    conn.close()
    return render_template_string(HTML_CONSOLE, instances=instances)

@app.route('/api/health')
def health():
    return jsonify({"platform": "SHMRY", "region": "Islamabad-A", "status": "ONLINE", "provider": "NIFDU"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
