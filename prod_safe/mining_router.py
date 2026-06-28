def enhanced_mining(query):
    q = query.lower()
    if any(k in q for k in ["mining", "s21", "monero"]):
        return """⛏️ SHMRY Mining Dashboard
- Process: Active (free solar power)
- Next: Add temperature/hashrate monitoring with your Antminer S21 and XMRig
- ROI tip: Track with solar 6kW + 700Ah bank"""
    return None
