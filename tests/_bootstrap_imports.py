import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MARKETPLACE = ROOT / "marketplace"

for p in [ROOT, MARKETPLACE]:
    s = str(p)
    if s not in sys.path:
        sys.path.insert(0, s)
