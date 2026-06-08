import sys
sys.path.append('/home/badrpk/shmry_cloud_hyperscale/marketplace')
from shmry_ai_layer import ask_shmry

print("======================================================================")
print("🧠 SHMRY INTELLIGENCE AGENT ENGINE: MULTI-PARTY SIMULATION RUNNER")
print("======================================================================\n")

print("🛒 [1/3] GENERATING BUYER D2C CONFIRMATION...")
buyer_prompt = "Generate a short message to customer Badar Zaman confirming his purchase order of a 5kW Solar Kit. Price: 215,000 PKR. Delivery location: Islamabad. Sound professional and reassuring."
print(ask_shmry(buyer_prompt))
print("\n" + "-"*50 + "\n")

print("🏭 [2/3] GENERATING B2B MANUFACTURER DISPATCH INSTRUCTION...")
seller_prompt = "Generate a quick alert to PakSolar Manufacturing Core. Their SKU D2C-5KW-INV has been matched to an order. Factory cost to payout is 180,000 PKR. Request stock preparation."
print(ask_shmry(seller_prompt))
print("\n" + "-"*50 + "\n")

print("🛵 [3/3] GENERATING LOGISTICS FREIGHT ROUTE DISPATCH...")
rider_prompt = "Generate an urgent dispatch text to Rawalpindi Fast Riders Core for a 15km haul to Islamabad. Freight fee allocation is 1,440 PKR. Request route confirmation."
print(ask_shmry(rider_prompt))
print("\n======================================================================")
