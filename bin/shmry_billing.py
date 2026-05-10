import sqlite3
import json
from pathlib import Path

DB = Path.home() / "shmry_cloud_hyperscale/vault/shmry_cloud.db"

# Pricing Table (Hourly PKR)
PRICING = {
    "enterprise": 500,
    "business": 250,
    "starter": 100
}

def generate_report():
    conn = sqlite3.connect(DB)
    cursor = conn.cursor()
    
    # Calculate revenue based on active instances and customer tiers
    query = """
    SELECT c.name, c.tier, COUNT(i.id) as instance_count
    FROM customers c
    LEFT JOIN instances i ON c.id = i.customer_id
    GROUP BY c.name
    """
    
    report = []
    total_pkr = 0
    
    for name, tier, count in cursor.execute(query).fetchall():
        rate = PRICING.get(tier.lower(), 100)
        hourly_revenue = count * rate
        total_pkr += hourly_revenue
        report.append({
            "customer": name,
            "tier": tier,
            "active_instances": count,
            "hourly_rate_pkr": rate,
            "hourly_total_pkr": hourly_revenue
        })
    
    conn.close()
    return {
        "region": "Islamabad-A",
        "currency": "PKR",
        "total_hourly_revenue": total_pkr,
        "total_monthly_projection": total_pkr * 24 * 30,
        "breakdown": report
    }

if __name__ == "__main__":
    print(json.dumps(generate_report(), indent=4))
