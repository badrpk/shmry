def crypto_value(query):
    q = query.lower()
    if any(word in q for word in ["mined", "value", "earnings", "pkr", "crypto"]):
        return """💰 SHMRY Crypto Mining Value (Estimate)
- Mining: Active on free solar power
- To get accurate PKR value: Connect your wallet/pool (Moneroocean, etc.)
- Next step: Share your pool username or wallet RPC details for real-time tracking
- Example: 0.001 XMR × current price × PKR rate"""
    return None
