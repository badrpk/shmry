import os
import http.client
import json

def get_gemini_key():
    env_path = "/home/badrpk/.env"
    if os.path.exists(env_path):
        with open(env_path, "r") as f:
            for line in f:
                if "SHMRY_API_KEY" in line:
                    return line.split("=")[1].strip()
    return None

def generate_human_message(target_role, entity_name, sku_title, price_or_profit):
    api_key = get_gemini_key()
    if not api_key:
        return f"System Alert [{target_role.upper()}]: Core transaction logged for {sku_title}."

    # Establish custom personalized prompts for your three multi-party anchors
    prompts = {
        "buyer": f"Write a friendly, polite SMS message to a Pakistani retail customer named {entity_name} confirming their order for '{sku_title}'. The final amount charged is {price_or_profit:,} PKR. Mention that a local delivery rider is already en-route from the factory line. Keep it professional, helpful, and concise.",
        "seller": f"Write a formal B2B alert notification message to our manufacturing partner '{entity_name}'. Inform them that their SKU variant '{sku_title}' has been successfully matched to an organic customer purchase request. Request immediate warehouse packaging release for the shipment batch. The wholesale payout is settled at {price_or_profit:,} PKR.",
        "rider": f"Write an urgent dispatch route notification message to our logistics driver '{entity_name}'. A flash distribution assignment is standing by for target SKU '{sku_title}'. Delivery payout matrix allocation locked at {price_or_profit:,} PKR. Request route navigation confirmation."
    }

    prompt_text = prompts.get(target_role.lower(), "Transaction verified.")
    
    # Configure low-overhead payload architecture for Gemini endpoint
    host = "generativelanguage.googleapis.com"
    endpoint = f"/v1beta/models/gemini-2.5-flash:generateContent?key={api_key}"
    
    headers = {"Content-Type": "application/json"}
    payload = {
        "contents": [{"parts": [{"text": prompt_text}]}]
    }

    try:
        conn = http.client.HTTPSConnection(host)
        conn.request("POST", endpoint, body=json.dumps(payload), headers=headers)
        res = conn.getresponse()
        data = json.loads(res.read().decode())
        conn.close()
        return data['candidates'][0]['content']['parts'][0]['text'].strip()
    except Exception as e:
        return f"🤖 SHMRY Dispatch Core: Order locked for {sku_title}. Value: {price_or_profit} PKR."

if __name__ == "__main__":
    print("=== TESTING BUYER ENGAGEMENT TEXT GENERATION ===")
    print(generate_human_message("buyer", "Badar Zaman", "Sovereign 5kW Smart Inverter", 215000))
