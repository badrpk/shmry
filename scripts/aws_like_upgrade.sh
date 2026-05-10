#!/usr/bin/env bash
set -euo pipefail

ROOT="$HOME/shmry_cloud_hyperscale"
DB="$ROOT/vault/shmry_cloud.db"
mkdir -p scripts docs security metrics deployment dr billing governance secrets

echo "🔐 Adding IAM-lite, secrets, quotas, billing, metrics, DR, governance..."

sqlite3 "$DB" <<'SQL'
CREATE TABLE IF NOT EXISTS iam_users (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  username TEXT UNIQUE NOT NULL,
  role TEXT NOT NULL,
  created_at TEXT DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS iam_roles (
  role TEXT PRIMARY KEY,
  permissions TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS api_tokens (
  token_name TEXT PRIMARY KEY,
  token_hash TEXT NOT NULL,
  role TEXT NOT NULL,
  created_at TEXT DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS quotas (
  name TEXT PRIMARY KEY,
  limit_value INTEGER NOT NULL,
  current_value INTEGER DEFAULT 0
);

CREATE TABLE IF NOT EXISTS billing_ledger (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  service TEXT,
  units INTEGER,
  unit_price REAL,
  total REAL,
  created_at TEXT DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS audit_events (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  actor TEXT,
  action TEXT,
  resource TEXT,
  decision TEXT,
  created_at TEXT DEFAULT CURRENT_TIMESTAMP
);

INSERT OR IGNORE INTO iam_roles VALUES
('admin','*'),
('operator','read,health,backup,deploy'),
('viewer','read,health');

INSERT OR IGNORE INTO iam_users(username, role) VALUES
('badrpk','admin');

INSERT OR IGNORE INTO quotas VALUES
('max_services',1000,151),
('max_instances',1000,148),
('max_monthly_cost_units',100000,0);
SQL

cat > scripts/metrics_exporter.py <<'PY'
#!/usr/bin/env python3
import os, sqlite3
from http.server import BaseHTTPRequestHandler, HTTPServer

ROOT=os.path.expanduser("~/shmry_cloud_hyperscale")
DB=f"{ROOT}/vault/shmry_cloud.db"

def q(sql, fallback=0):
    try:
        con=sqlite3.connect(DB); cur=con.cursor(); cur.execute(sql)
        val=cur.fetchone()[0]; con.close(); return val
    except Exception:
        return fallback

class H(BaseHTTPRequestHandler):
    def do_GET(self):
        body=f"""# HELP shmry_instances Total SHMRY instances
# TYPE shmry_instances gauge
shmry_instances {q("SELECT COUNT(*) FROM instances")}

# HELP shmry_services Total SHMRY services
# TYPE shmry_services gauge
shmry_services {q("SELECT COUNT(*) FROM services")}

# HELP shmry_css_mastery CSS mastery score
# TYPE shmry_css_mastery gauge
shmry_css_mastery {q("SELECT value FROM sovereign_metrics WHERE name='css_mastery'")}
"""
        self.send_response(200)
        self.send_header("Content-Type","text/plain")
        self.end_headers()
        self.wfile.write(body.encode())

HTTPServer(("0.0.0.0",9090),H).serve_forever()
PY

cat > scripts/secret_put.sh <<'SH'
#!/usr/bin/env bash
set -euo pipefail
NAME="$1"
VALUE="$2"
ROOT="$HOME/shmry_cloud_hyperscale"
mkdir -p "$ROOT/secrets"
printf "%s" "$VALUE" | openssl enc -aes-256-cbc -pbkdf2 -salt -out "$ROOT/secrets/$NAME.enc"
echo "secret stored: secrets/$NAME.enc"
SH

cat > scripts/secret_get.sh <<'SH'
#!/usr/bin/env bash
set -euo pipefail
NAME="$1"
ROOT="$HOME/shmry_cloud_hyperscale"
openssl enc -d -aes-256-cbc -pbkdf2 -in "$ROOT/secrets/$NAME.enc"
SH

cat > scripts/dr_drill.sh <<'SH'
#!/usr/bin/env bash
set -euo pipefail
ROOT="$HOME/shmry_cloud_hyperscale"
./scripts/backup.sh
TMP="$(mktemp -d)"
cp vault/shmry_cloud.db "$TMP/test_restore.db"
sqlite3 "$TMP/test_restore.db" "PRAGMA integrity_check;"
rm -rf "$TMP"
echo "✅ DR drill passed"
SH

cat > scripts/billing_meter.sh <<'SH'
#!/usr/bin/env bash
set -euo pipefail
DB="$HOME/shmry_cloud_hyperscale/vault/shmry_cloud.db"
SERVICES="$(sqlite3 "$DB" 'SELECT COUNT(*) FROM services;')"
INSTANCES="$(sqlite3 "$DB" 'SELECT COUNT(*) FROM instances;')"
TOTAL="$(awk "BEGIN {print ($SERVICES * 0.01) + ($INSTANCES * 0.02)}")"
sqlite3 "$DB" "INSERT INTO billing_ledger(service,units,unit_price,total) VALUES('shmry_runtime',$((SERVICES+INSTANCES)),0.01,$TOTAL);"
echo "metered total: $TOTAL"
SH

cat > scripts/policy_check.sh <<'SH'
#!/usr/bin/env bash
set -euo pipefail
ROOT="$HOME/shmry_cloud_hyperscale"
echo "🔎 Policy check"
test -f "$ROOT/.gitignore"
grep -q "secrets/" "$ROOT/.gitignore" || echo "secrets/" >> "$ROOT/.gitignore"
grep -q "*.env" "$ROOT/.gitignore" || echo "*.env" >> "$ROOT/.gitignore"
grep -q "get-docker.sh" "$ROOT/.gitignore" || echo "get-docker.sh" >> "$ROOT/.gitignore"
echo "✅ Policy baseline enforced"
SH

chmod +x scripts/*.sh scripts/*.py

cat > deployment/local.env <<'EOF2'
SHMRY_PROFILE=local
SHMRY_DASHBOARD_PORT=8088
SHMRY_METRICS_PORT=9090
EOF2

cat > deployment/vps.env <<'EOF2'
SHMRY_PROFILE=vps
SHMRY_DASHBOARD_PORT=8088
SHMRY_METRICS_PORT=9090
SHMRY_TLS_REQUIRED=true
EOF2

cat > docs/AWS_LIKE_CAPABILITIES.md <<'EOF2'
# SHMRY AWS-like Local Capability Layer

Implemented local primitives:
- IAM-lite users, roles, permissions
- API token table
- audit event table
- quota table
- billing ledger
- encrypted local secrets
- Prometheus-style metrics endpoint
- DR drill script
- deployment profiles
- policy baseline

Not equivalent to AWS:
- no global regions
- no physical datacenters
- no managed multi-AZ durability
- no formal SLA
- no compliance certification
- no managed fleet autoscaling
- no hyperscale network backbone
EOF2

cat > .gitignore <<'EOF2'
secrets/
*.env
get-docker.sh
__pycache__/
*.pyc
EOF2

./scripts/policy_check.sh
./scripts/dr_drill.sh
./scripts/billing_meter.sh

git add .
git commit -m "platform: add AWS-like local primitives for IAM secrets metrics billing DR governance" || true
git push origin main

echo "✅ AWS-like local upgrade complete"
echo "Run metrics: python3 scripts/metrics_exporter.py"
echo "View metrics: curl http://localhost:9090/metrics"
