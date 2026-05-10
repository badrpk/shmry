#!/usr/bin/env bash
set -euo pipefail

ROOT="$HOME/shmry_cloud_hyperscale"
DB="$ROOT/vault/shmry_cloud.db"
OUT="$ROOT/docs/AWS_GAP_AUDIT.md"

mkdir -p "$ROOT/docs"

check_file() {
  [ -e "$ROOT/$1" ] && echo "✅ Present" || echo "❌ Missing"
}

check_cmd() {
  command -v "$1" >/dev/null 2>&1 && echo "✅ Present" || echo "❌ Missing"
}

check_port() {
  curl -fsS "$1" >/dev/null 2>&1 && echo "✅ Responding" || echo "❌ Not responding"
}

{
echo "# SHMRY vs AWS Capability Gap Audit"
echo
echo "Generated: $(date -Is)"
echo
echo "## Current SHMRY Baseline"
echo
echo "- Git commit: $(git -C "$ROOT" rev-parse --short HEAD)"
echo "- Git status: $(git -C "$ROOT" status --short | wc -l) changed files"
echo "- Instances: $(sqlite3 "$DB" "SELECT COUNT(*) FROM instances;" 2>/dev/null || echo unknown)"
echo "- Services: $(sqlite3 "$DB" "SELECT COUNT(*) FROM services;" 2>/dev/null || echo unknown)"
echo "- CSS mastery: $(sqlite3 "$DB" "SELECT value FROM sovereign_metrics WHERE name='css_mastery';" 2>/dev/null || echo unknown)"
echo

echo "## AWS-Class Capability Matrix"
echo
echo "| Capability | SHMRY Evidence | Status |"
echo "|---|---:|---|"
echo "| Reproducible deployment | Dockerfile / compose | $(check_file Dockerfile) |"
echo "| Runbook documentation | docs/RUNBOOK.md | $(check_file docs/RUNBOOK.md) |"
echo "| Architecture documentation | docs/ARCHITECTURE.md | $(check_file docs/ARCHITECTURE.md) |"
echo "| Healthcheck script | scripts/healthcheck.sh | $(check_file scripts/healthcheck.sh) |"
echo "| Backup script | scripts/backup.sh | $(check_file scripts/backup.sh) |"
echo "| Restore script | scripts/restore_latest.sh | $(check_file scripts/restore_latest.sh) |"
echo "| Test suite | tests/ | $(check_file tests) |"
echo "| CI workflow | .github/workflows/ci.yml | $(check_file .github/workflows/ci.yml) |"
echo "| Local dashboard | observability/dashboard.py | $(check_file observability/dashboard.py) |"
echo "| Pulse API | localhost:5000/pulse | $(curl -fsS -H "X-NIFDU-Token: EVOLVE_2026" http://localhost:5000/pulse >/dev/null 2>&1 && echo "✅ Responding" || echo "❌ Not responding") |"
echo "| Docker installed | docker CLI | $(check_cmd docker) |"
echo "| Compose installed | docker compose | $(docker compose version >/dev/null 2>&1 && echo "✅ Present" || echo "❌ Missing") |"
echo

echo "## Major Things AWS Has That SHMRY Likely Still Lacks"
echo
echo "### 1. Global physical infrastructure"
echo "- AWS has global regions, availability zones, edge networks, and managed datacenters."
echo "- SHMRY appears local-first unless deployed to external hosts."
echo
echo "### 2. Managed identity and access management"
echo "- Missing equivalent of IAM users, roles, policies, temporary credentials, MFA enforcement, and fine-grained authorization."
echo
echo "### 3. Multi-tenant isolation"
echo "- Missing hardened account boundaries, VPC-style network isolation, per-tenant quotas, and blast-radius controls."
echo
echo "### 4. Managed compute orchestration"
echo "- Missing EC2/ECS/EKS/Lambda equivalents with autoscaling, scheduling, placement, and self-healing."
echo
echo "### 5. Managed networking"
echo "- Missing VPCs, security groups, load balancers, private endpoints, DNS management, WAF, CDN, and DDoS protection."
echo
echo "### 6. Managed databases and storage"
echo "- SQLite is useful locally, but SHMRY lacks S3/EBS/EFS/RDS/DynamoDB-style durability, replication, lifecycle policies, and point-in-time recovery."
echo
echo "### 7. Observability depth"
echo "- Current dashboard is local. Missing CloudWatch-style metrics, logs, traces, alarms, retention, dashboards, and incident notifications."
echo
echo "### 8. Secrets management"
echo "- Missing KMS/Secrets Manager/Parameter Store equivalents for encryption, key rotation, and audited secret access."
echo
echo "### 9. Compliance and governance"
echo "- Missing audit trails, policy enforcement, config rules, asset inventory, compliance reports, and formal control mapping."
echo
echo "### 10. Billing and quotas"
echo "- Missing metering, budgets, cost allocation, usage quotas, and chargeback/showback."
echo
echo "### 11. Marketplace/ecosystem"
echo "- Missing managed partner integrations, marketplace deployment templates, SDKs, public APIs, and customer onboarding workflows."
echo
echo "### 12. SLA-grade operations"
echo "- Missing formal uptime targets, SLOs, alert escalation, disaster recovery drills, runbook automation, and support processes."
echo

echo "## Highest-Value Next Builds"
echo
echo "1. Add IAM-lite: users, roles, tokens, permissions table."
echo "2. Move runtime DB writes out of Git-tracked SQLite or separate config DB from event DB."
echo "3. Add Prometheus-compatible metrics endpoint."
echo "4. Add encrypted backups with restore testing."
echo "5. Add systemd user services for pulse, dashboard, and intelligence loop."
echo "6. Add deployment profiles: local, docker, VPS."
echo "7. Add API documentation and external onboarding guide."
echo "8. Add secret scanning and .gitignore protection for volatile state."
echo
} > "$OUT"

echo "✅ AWS gap audit written to: $OUT"
cat "$OUT"

git add scripts/aws_gap_audit.sh docs/AWS_GAP_AUDIT.md
git commit -m "audit: add AWS capability gap report" || true
git status
