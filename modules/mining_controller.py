"""
Minimal, robust mining status. No external dep until we add it properly.
"""
import subprocess
import json

def get_mining_status():
    """Return XMRig status or fallback."""
    try:
        # Quick check if XMRig is running
        result = subprocess.run(["pgrep", "-f", "xmrig"], capture_output=True, text=True)
        if result.returncode == 0:
            return {
                "status": "running",
                "pid": result.stdout.strip(),
                "note": "XMRig detected via pgrep"
            }
        return {"status": "offline"}
    except Exception as e:
        return {"status": "error", "error": str(e)}
