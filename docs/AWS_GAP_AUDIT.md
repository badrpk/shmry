# SHMRY vs AWS Capability Gap Audit

Generated: 2026-05-10T21:11:55+05:00

## Current SHMRY Baseline

- Git commit: aa781a7
- Git status: 3 changed files
- Instances: 148
- Services: 151
- CSS mastery: 0.85

## AWS-Class Capability Matrix

| Capability | SHMRY Evidence | Status |
|---|---:|---|
| Reproducible deployment | Dockerfile / compose | ✅ Present |
| Runbook documentation | docs/RUNBOOK.md | ✅ Present |
| Architecture documentation | docs/ARCHITECTURE.md | ✅ Present |
| Healthcheck script | scripts/healthcheck.sh | ✅ Present |
| Backup script | scripts/backup.sh | ✅ Present |
| Restore script | scripts/restore_latest.sh | ✅ Present |
| Test suite | tests/ | ✅ Present |
| CI workflow | .github/workflows/ci.yml | ✅ Present |
| Local dashboard | observability/dashboard.py | ✅ Present |
| Pulse API | localhost:5000/pulse | ✅ Responding |
| Docker installed | docker CLI | ❌ Missing |
| Compose installed | docker compose | ❌ Missing |

## Major Things AWS Has That SHMRY Likely Still Lacks

### 1. Global physical infrastructure
- AWS has global regions, availability zones, edge networks, and managed datacenters.
- SHMRY appears local-first unless deployed to external hosts.

### 2. Managed identity and access management
- Missing equivalent of IAM users, roles, policies, temporary credentials, MFA enforcement, and fine-grained authorization.

### 3. Multi-tenant isolation
- Missing hardened account boundaries, VPC-style network isolation, per-tenant quotas, and blast-radius controls.

### 4. Managed compute orchestration
- Missing EC2/ECS/EKS/Lambda equivalents with autoscaling, scheduling, placement, and self-healing.

### 5. Managed networking
- Missing VPCs, security groups, load balancers, private endpoints, DNS management, WAF, CDN, and DDoS protection.

### 6. Managed databases and storage
- SQLite is useful locally, but SHMRY lacks S3/EBS/EFS/RDS/DynamoDB-style durability, replication, lifecycle policies, and point-in-time recovery.

### 7. Observability depth
- Current dashboard is local. Missing CloudWatch-style metrics, logs, traces, alarms, retention, dashboards, and incident notifications.

### 8. Secrets management
- Missing KMS/Secrets Manager/Parameter Store equivalents for encryption, key rotation, and audited secret access.

### 9. Compliance and governance
- Missing audit trails, policy enforcement, config rules, asset inventory, compliance reports, and formal control mapping.

### 10. Billing and quotas
- Missing metering, budgets, cost allocation, usage quotas, and chargeback/showback.

### 11. Marketplace/ecosystem
- Missing managed partner integrations, marketplace deployment templates, SDKs, public APIs, and customer onboarding workflows.

### 12. SLA-grade operations
- Missing formal uptime targets, SLOs, alert escalation, disaster recovery drills, runbook automation, and support processes.

## Highest-Value Next Builds

1. Add IAM-lite: users, roles, tokens, permissions table.
2. Move runtime DB writes out of Git-tracked SQLite or separate config DB from event DB.
3. Add Prometheus-compatible metrics endpoint.
4. Add encrypted backups with restore testing.
5. Add systemd user services for pulse, dashboard, and intelligence loop.
6. Add deployment profiles: local, docker, VPS.
7. Add API documentation and external onboarding guide.
8. Add secret scanning and .gitignore protection for volatile state.

