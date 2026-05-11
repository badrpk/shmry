#!/usr/bin/env bash
set -euo pipefail

DB="vault/shmry_cloud.db"

echo "=== SHMRY PRODUCT AUDIT ==="

sqlite3 -header -column "$DB" "
SELECT name, value
FROM sovereign_metrics
WHERE name IN ('css_mastery','active_context','market_volatility');
"

echo
echo "=== PLATFORM STATUS ==="

sqlite3 -header -column "$DB" "
SELECT
 (SELECT COUNT(*) FROM instances) AS total_instances,
 (SELECT COUNT(*) FROM instances WHERE status='RUNNING') AS running_instances,
 (SELECT COUNT(*) FROM services) AS total_services,
 (SELECT SUM(amount) FROM invoices WHERE status='PAID') AS paid_revenue;
"

echo
echo "=== REGIONAL TOPOLOGY ==="

sqlite3 -header -column "$DB" "
SELECT region, COUNT(*) AS nodes
FROM instances
WHERE status='RUNNING'
GROUP BY region
ORDER BY nodes DESC;
"
