import requests, json, time, random
from concurrent.futures import ThreadPoolExecutor, as_completed

BASE_URL = "http://127.0.0.1:5000"
TOKEN = "YOUR_JWT_TOKEN_HERE"  # Replace

headers = {
    "Authorization": f"Bearer {TOKEN}",
    "Content-Type": "application/json"
}

def create_rfq():
    payload = {
        "item": random.choice(["Rebar 12mm", "Billet 100x100", "Wire Rod 8mm"]),
        "quantity": random.randint(100, 1000),
        "budget": random.randint(200000, 800000)
    }
    try:
        r = requests.post(f"{BASE_URL}/steel/rfq", json=payload, headers=headers, timeout=5)
        return r.json().get("rfq_id") if r.status_code == 200 else None
    except:
        return None

def submit_bid(rfq_id):
    payload = {
        "rfq_id": rfq_id,
        "amount": random.randint(180000, 750000),
        "delivery_days": random.randint(5, 15)
    }
    try:
        requests.post(f"{BASE_URL}/steel/bid", json=payload, headers=headers, timeout=5)
    except:
        pass

def run_load_test(num_requests=100, max_workers=20):
    print(f"Load test: {num_requests} RFQs, {max_workers} workers")
    start = time.time()
    
    rfq_ids = []
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        # Create RFQs
        futures = [executor.submit(create_rfq) for _ in range(num_requests)]
        for future in as_completed(futures):
            rfq_id = future.result()
            if rfq_id:
                rfq_ids.append(rfq_id)
        
        # Submit bids
        bid_futures = [executor.submit(submit_bid, rfq_id) for rfq_id in rfq_ids]
        for future in as_completed(bid_futures):
            pass  # fire and forget
    
    duration = time.time() - start
    print(f"Completed in {duration:.2f}s | RPS: {num_requests / duration:.2f}")
    print(f"Successful RFQs: {len(rfq_ids)}")

if __name__ == "__main__":
    run_load_test(num_requests=200, max_workers=30)
