# SHMRY Cloud Architecture

SHMRY is a local-first infrastructure control plane.

Components:
- vault/shmry_cloud.db: SQLite state vault
- logs/shmry_intelligence.log: intelligence audit log
- /pulse: local pulse API
- scripts/: health, backup, restore operations
- observability/: local dashboard
- tests/: repeatable verification
