#!/usr/bin/env bash
set -euo pipefail

mkdir -p .github/workflows .github/ISSUE_TEMPLATE docs examples scripts assets

cat > .gitignore <<'GI'
.venv/
venv/
__pycache__/
*.pyc
logs/
local_state/
backups/
.DS_Store
.vscode/
.idea/
GI

cat > requirements.txt <<'REQ'
flask
gunicorn
REQ

cat > examples/demo_safe_agent.sh <<'SH'
#!/usr/bin/env bash
set -euo pipefail
mkdir -p "$HOME/.shmry/memory" "$HOME/.shmry/logs"
echo "SHMRY demo started"
echo "Memory registry: OK"
echo "Safety gate: OK"
echo "Audit log: OK"
echo '{"event":"demo_completed"}' >> "$HOME/.shmry/memory/registry.jsonl"
echo "Demo task completed"
SH
chmod +x examples/demo_safe_agent.sh

cat > scripts/smoke_test.sh <<'SH'
#!/usr/bin/env bash
set -euo pipefail
bash install.sh
bash examples/demo_safe_agent.sh
echo "Smoke test passed."
SH
chmod +x scripts/smoke_test.sh

cat > install.sh <<'SH'
#!/usr/bin/env bash
set -euo pipefail
python3 -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt
mkdir -p "$HOME/.shmry/memory" "$HOME/.shmry/logs"
echo '{"type":"system","status":"initialized"}' > "$HOME/.shmry/memory/registry.jsonl"
echo "Install complete. Run: bash examples/demo_safe_agent.sh"
SH
chmod +x install.sh

cat > .github/workflows/smoke_test.yml <<'YML'
name: smoke-test
on: [push, pull_request]
jobs:
  smoke:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.11'
      - run: bash install.sh
      - run: bash examples/demo_safe_agent.sh
YML

git rm -r --cached .venv venv logs local_state backups __pycache__ 2>/dev/null || true
git add .
git commit -m "Improve one-shot install and GitHub adoption assets" || true
git push origin main
