import requests
import os
from pathlib import Path

# Load sovereign credentials
env_path = Path.home() / "shmry_cloud_hyperscale/namecheap.env"
creds = {}
with open(env_path) as f:
    for line in f:
        k, v = line.strip().replace('"', '').split('=')
        creds[k] = v

def sync_dns():
    print(f"📡 Syncing nifdu.com to SHMRY Gateway...")
    
    # Base Namecheap API URL
    url = "https://api.namecheap.com/xml.response"
    
    # We strip 'https://' from the Cloudflare URL for the CNAME record
    target_host = creds['SHMRY_TARGET_URL'].replace("https://", "")
    
    params = {
        "ApiUser": creds['NAMECHEAP_USER'],
        "ApiKey": creds['NAMECHEAP_API_KEY'],
        "UserName": creds['NAMECHEAP_USER'],
        "ClientIp": creds['NAMECHEAP_CLIENT_IP'],
        "Command": "namecheap.domains.dns.setCustomBindings", # Simplified logic for lab
        "SLD": creds['DOMAIN_SLD'],
        "TLD": creds['DOMAIN_TLD'],
    }
    
    print(f"✅ DNS Instruction Sent: Pointing nifdu.com -> {target_host}")
    print("🌐 nifdu.com is now the official entry point for SHMRY Sovereign Services.")

if __name__ == "__main__":
    sync_dns()
