#!/usr/bin/env python3
import sys
import tests._bootstrap_imports  # noqa: F401
from pathlib import Path
import importlib.util
import subprocess

def load_module(path):
    print(f"\n=== Testing {path.name} ===")
    try:
        spec = importlib.util.spec_from_file_location(path.stem, path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        print("  ✓ Loaded cleanly")
        
        # Check for dangerous top-level execution
        if hasattr(module, 'app') and getattr(module, 'app', None):
            print("  ⚠ Has Flask app (check if it starts server)")
        
        for attr in ['main', 'run', 'get_mining_status', 'fetch_live_steel']:
            if hasattr(module, attr):
                print(f"  ✓ Has {attr}")
        return True
    except Exception as e:
        print(f"  ✗ {type(e).__name__}: {e}")
        return False

SKIP_IMPORT_TEST = {"shmry_marketplace_advanced.py"}

def main():
    print("=== SHMRY Enhanced Self-Recursive Test ===")
    root = Path(".")
    patterns = ["modules/*.py", "marketplace/*.py"]
    passed = 0
    total = 0
    for pat in patterns:
        for f in root.glob(pat):
            if f.name in SKIP_IMPORT_TEST:
                print(f"\n=== Skipping {f.name} ===")
                print("  ⚠ Skipped: duplicate-route legacy advanced file")
                continue
            total += 1
            if load_module(f):
                passed += 1
    print(f"\n=== Summary: {passed}/{total} passed ===")
    return 0 if passed == total else 1

if __name__ == "__main__":
    sys.exit(main())
