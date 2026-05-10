import os
from pathlib import Path

VAULT_PATH = Path.home() / "shmry_cloud_hyperscale/vault"

def get_bucket_stats():
    files = list(VAULT_PATH.glob("*"))
    total_size = sum(f.stat().st_size for f in files if f.is_file())
    return {
        "bucket_name": "nifdu-primary-vault",
        "object_count": len(files),
        "total_size_mb": round(total_size / (1024 * 1024), 2),
        "region": "pk-islamabad-1"
    }

if __name__ == "__main__":
    print(get_bucket_stats())
