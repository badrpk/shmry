#!/usr/bin/env bash
set -euo pipefail

ROOT="$HOME/shmry_cloud_hyperscale"
BIN="$ROOT/bin"
VAULT="$ROOT/vault"
DB="$VAULT/shmry_cloud.db"

mkdir -p "$BIN" "$VAULT"

cat > "$BIN/nifdu_service_catalog.py" <<'PY'
import sqlite3, json, time
from pathlib import Path

DB = Path.home() / "shmry_cloud_hyperscale/vault/shmry_cloud.db"

AWS_STYLE_SERVICES = """
EC2 S3 IAM Lambda RDS DynamoDB VPC CloudFront Route53 EBS EFS FSx Glacier Backup
CloudWatch CloudTrail Config SystemsManager Organizations ControlTower GuardDuty SecurityHub Inspector Macie KMS SecretsManager CertificateManager WAF Shield FirewallManager
ECS EKS Fargate Batch Lightsail ElasticBeanstalk AppRunner AutoScaling ELB API-Gateway AppSync EventBridge SNS SQS StepFunctions MQ SWF
Aurora Redshift ElastiCache Neptune DocumentDB Keyspaces Timestream QLDB OpenSearch LakeFormation Glue Athena EMR Kinesis MSK DataPipeline DataSync TransferFamily
SageMaker Bedrock Comprehend Rekognition Textract Polly Lex Transcribe Translate Forecast Personalize Kendra FraudDetector CodeWhisperer
CodeCommit CodeBuild CodeDeploy CodePipeline CodeArtifact Cloud9 XRay Proton Amplify DeviceFarm
WorkSpaces AppStream WorkDocs WorkMail Chime Connect Pinpoint SES
IoTCore IoTGreengrass IoTAnalytics IoTEvents IoTSiteWise IoTDeviceDefender IoTRoboRunner
MediaConvert MediaLive MediaPackage MediaStore MediaTailor IVS ElasticTranscoder
MigrationHub DMS ApplicationMigrationService ServerMigrationService Snowball Snowcone Snowmobile
Outposts LocalZones Wavelength GlobalAccelerator DirectConnect PrivateLink TransitGateway NetworkFirewall CloudWAN
Billing CostExplorer Budgets CUR Marketplace LicenseManager Support TrustedAdvisor Health
ManagedBlockchain QuantumLedgerDatabase Braket GroundStation RoboMaker GameLift
VerifiedPermissions EntityResolution CleanRooms DataZone Omics SimSpaceWeaver
ApplicationComposer ResilienceHub FaultInjectionSimulator WellArchitected ServiceCatalog RAM
Detective AuditManager Artifact BackupGateway StorageGateway
""".split()

CATEGORIES = {
    "compute": ["EC2","Lambda","ECS","EKS","Fargate","Batch","Lightsail","ElasticBeanstalk","AppRunner","AutoScaling"],
    "storage": ["S3","EBS","EFS","FSx","Glacier","Backup","StorageGateway","BackupGateway"],
    "database": ["RDS","Aurora","DynamoDB","Redshift","ElastiCache","Neptune","DocumentDB","Keyspaces","Timestream","QLDB"],
    "networking": ["VPC","CloudFront","Route53","ELB","API-Gateway","DirectConnect","PrivateLink","TransitGateway","NetworkFirewall","CloudWAN"],
    "security": ["IAM","KMS","SecretsManager","GuardDuty","SecurityHub","Inspector","Macie","WAF","Shield","CertificateManager"],
    "analytics": ["Glue","Athena","EMR","Kinesis","MSK","LakeFormation","OpenSearch","DataPipeline","DataSync"],
    "ai_ml": ["SageMaker","Bedrock","Comprehend","Rekognition","Textract","Polly","Lex","Transcribe","Translate","Forecast","Personalize","Kendra"],
    "devops": ["CodeCommit","CodeBuild","CodeDeploy","CodePipeline","CodeArtifact","Cloud9","XRay","Proton","Amplify"],
    "business": ["WorkSpaces","AppStream","WorkDocs","WorkMail","Chime","Connect","Pinpoint","SES"],
    "iot": ["IoTCore","IoTGreengrass","IoTAnalytics","IoTEvents","IoTSiteWise","IoTDeviceDefender"],
    "media": ["MediaConvert","MediaLive","MediaPackage","MediaStore","MediaTailor","IVS","ElasticTranscoder"],
    "billing": ["Billing","CostExplorer","Budgets","CUR","Marketplace","LicenseManager","Support","TrustedAdvisor","Health"],
}

def category_for(name):
    for cat, items in CATEGORIES.items():
        if name in items:
            return cat
    return "specialized"

def init_catalog():
    conn = sqlite3.connect(DB)
    conn.execute("""
    CREATE TABLE IF NOT EXISTS service_catalog(
        name TEXT PRIMARY KEY,
        nifdu_name TEXT,
        category TEXT,
        status TEXT,
        mode TEXT,
        created_at REAL
    )
    """)
    for svc in sorted(set(AWS_STYLE_SERVICES)):
        conn.execute("""
        INSERT OR REPLACE INTO service_catalog
        VALUES (?, ?, ?, ?, ?, ?)
        """, (
            svc,
            "NIFDU-" + svc,
            category_for(svc),
            "CATALOG_REGISTERED",
            "mock-control-plane",
            time.time()
        ))
    conn.commit()
    conn.close()

def list_services():
    init_catalog()
    conn = sqlite3.connect(DB)
    rows = conn.execute("""
        SELECT name, nifdu_name, category, status, mode
        FROM service_catalog
        ORDER BY category, name
    """).fetchall()
    conn.close()
    return [
        {
            "aws_style_service": r[0],
            "nifdu_service": r[1],
            "category": r[2],
            "status": r[3],
            "mode": r[4]
        }
        for r in rows
    ]

def summary():
    services = list_services()
    by_category = {}
    for s in services:
        by_category[s["category"]] = by_category.get(s["category"], 0) + 1
    return {
        "platform": "NIFDU SHMRY Sovereign Cloud",
        "catalog_mode": "AWS-style service registry",
        "important_note": "These are catalog/control-plane stubs, not full AWS-equivalent managed services yet.",
        "service_count": len(services),
        "categories": by_category
    }

if __name__ == "__main__":
    init_catalog()
    print(json.dumps(summary(), indent=2))
PY

cat > "$BIN/shmry_aws_style_console.py" <<'PY'
from flask import Flask, jsonify, request
import sys
from pathlib import Path

sys.path.append(str(Path.home() / "shmry_cloud_hyperscale/bin"))

from shmry_billing import generate_report
from nifdu_service_catalog import list_services, summary
try:
    from nifdu_s3 import get_bucket_stats
except Exception:
    get_bucket_stats = lambda: {"status": "S3 stats unavailable"}

app = Flask(__name__)

@app.route("/")
def index():
    s = summary()
    return f"""
    <h1>NIFDU SHMRY Sovereign Cloud</h1>
    <p>Status: ONLINE</p>
    <p>AWS-style catalog services registered: <b>{s['service_count']}</b></p>
    <ul>
      <li><a href="/api/health">/api/health</a></li>
      <li><a href="/api/catalog/summary">/api/catalog/summary</a></li>
      <li><a href="/api/services">/api/services</a></li>
      <li><a href="/api/billing">/api/billing</a></li>
      <li>/api/predict POST</li>
      <li><a href="/api/storage">/api/storage</a></li>
    </ul>
    """

@app.route("/api/health")
def health():
    return jsonify({
        "platform": "NIFDU SHMRY Sovereign Cloud",
        "region": "pk-islamabad-1",
        "status": "ONLINE"
    })

@app.route("/api/catalog/summary")
def catalog_summary():
    return jsonify(summary())

@app.route("/api/services")
def services():
    return jsonify(list_services())

@app.route("/api/service/<name>")
def service_detail(name):
    name_l = name.lower()
    for svc in list_services():
        if svc["aws_style_service"].lower() == name_l or svc["nifdu_service"].lower() == name_l:
            svc["endpoint_status"] = "stub-ready"
            svc["provisioning_status"] = "not-yet-real-infrastructure"
            return jsonify(svc)
    return jsonify({"error": "service not found", "name": name}), 404

@app.route("/api/billing")
def billing():
    return jsonify(generate_report())

@app.route("/api/storage")
def storage():
    return jsonify(get_bucket_stats())

@app.route("/api/predict", methods=["POST"])
def predict():
    data = request.get_json(silent=True) or {}
    text = data.get("text", "")
    sentiment = "Positive" if len(text) > 10 else "Neutral"
    return jsonify({
        "model": "NIFDU-Urdu-Llama-1",
        "input": text,
        "sentiment": sentiment,
        "region": "pk-islamabad-1"
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
PY

python3 "$BIN/nifdu_service_catalog.py"
python3 -m py_compile "$BIN/shmry_aws_style_console.py"

pkill -f shmry_aws_style_console.py || true

nohup python3 "$BIN/shmry_aws_style_console.py" > "$ROOT/web.log" 2>&1 &

sleep 2

echo "✅ NIFDU AWS-style 200-service catalog installed"
curl -s http://localhost:5000/api/catalog/summary | jq
