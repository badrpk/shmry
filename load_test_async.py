import asyncio
import aiohttp
import json
import random
import time

BASE_URL = "http://127.0.0.1:5000"
TOKEN = "YOUR_JWT_TOKEN_HERE"  # Replace with valid token

headers = {
    "Authorization": f"Bearer {TOKEN}",
    "Content-Type": "application/json"
}

async def create_rfq(session):
    payload = {
        "item": random.choice(["Rebar 12mm", "Billet 100x100", "Wire Rod 8mm"]),
        "quantity": random.randint(100, 1000),
        "budget": random.randint(200000, 800000)
    }
    try:
        async with session.post(f"{BASE_URL}/steel/rfq", json=payload, headers=headers) as resp:
            if resp.status == 200:
                data = await resp.json()
                return data.get("rfq_id")
    except:
        return None

async def submit_bid(session, rfq_id):
    payload = {
        "rfq_id": rfq_id,
        "amount": random.randint(180000, 750000),
        "delivery_days": random.randint(5, 15)
    }
    try:
        async with session.post(f"{BASE_URL}/steel/bid", json=payload, headers=headers) as resp:
            pass
    except:
        pass

async def run_load_test(num_requests=200, concurrency=50):
    print(f"Async load test: {num_requests} RFQs, concurrency={concurrency}")
    start = time.time()
    rfq_ids = []
    
    async with aiohttp.ClientSession() as session:
        # Create RFQs
        tasks = [create_rfq(session) for _ in range(num_requests)]
        results = await asyncio.gather(*tasks)
        rfq_ids = [r for r in results if r]
        
        # Submit bids
        bid_tasks = [submit_bid(session, rfq_id) for rfq_id in rfq_ids]
        await asyncio.gather(*bid_tasks)
    
    duration = time.time() - start
    print(f"Completed in {duration:.2f}s | RPS: {num_requests / duration:.2f}")
    print(f"Successful RFQs: {len(rfq_ids)}")

if __name__ == "__main__":
    asyncio.run(run_load_test(num_requests=300, concurrency=60))
