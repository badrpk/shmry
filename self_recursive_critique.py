#!/usr/bin/env python3
import sys
from pathlib import Path
import importlib.util

def load_and_test(path):
    print(f"\n=== {path} ===")
    try:
        spec = importlib.util.spec_from_file_location(path.stem, path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        print("  ✓ Loaded cleanly")
        entry = any(hasattr(module, a) for a in ['main','run','app'])
        if entry:
            print("  ✓ Has entry point")
        return True
    except Exception as e:
        print(f"  ✗ {type(e).__name__}: {e}")
        return False

def main():
    print("=== SHMRY Recursive Critique ===")
    root = Path(".")
    SKIP={"shmry_gateway_clean_v19.py","shmry_marketplace.py"}
    candidates = []
    for pat in ["modules/*.py", "marketplace/*.py", "*.py"]:
        candidates.extend(root.glob(pat))
    
    passed = sum(1 for p in candidates[:15] if p.name not in SKIP and load_and_test(p))  # limit to avoid explosion
    print(f"\nSummary: {passed} passed (sampled)")
    print("Run with full path if you want deeper analysis.")
    return 0

if __name__ == "__main__":
    sys.exit(main())

# Kernel integration
try:
    from core.kernel import SHMRYKernel
    kernel = SHMRYKernel()
    kernel.mutate("Improved import safety + kernel awareness")
    kernel.report()
except Exception as e:
    print(f"Kernel integration issue: {e}")
