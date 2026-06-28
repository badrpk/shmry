#!/home/badrpk/shmry_10of10/venv/bin/python
#!/usr/bin/env python3

# ==== SHMRY SELF-AWARENESS PREEMPT v1 ====
def __shmry_self_awareness_preempt(user_query):
    import os, subprocess, time
    from pathlib import Path

    q = (user_query or "").lower().strip()
    home = str(Path.home())

    def run(cmd, timeout=6):
        try:
            return subprocess.check_output(cmd, shell=True, text=True, stderr=subprocess.DEVNULL, timeout=timeout).strip()
        except Exception as e:
            return ""

    if any(x in q for x in ["how are you", "status", "health", "operational"]):
        uptime = run("uptime -p")
        disk = run("df -h $HOME | tail -1 | awk '{print $3\" used / \"$2\" total (\"$5\")\"}'")
        ram = run("free -h | awk '/Mem:/ {print $3\" used / \"$2\" total\"}'")
        py = run("python3 --version")
        procs = run("ps -u $USER -o comm= | sort | uniq | grep -Ei 'python|caddy|node|sqlite|shmry' | head -20")
        return f"""✅ SHMRY Operational

Runtime:
- Uptime: {uptime or 'unknown'}
- RAM: {ram or 'unknown'}
- Disk: {disk or 'unknown'}
- Python: {py or 'unknown'}

Detected services/processes:
{procs or 'No SHMRY-related process detected by name.'}

I am not just a generic chatbot here; I can inspect local runtime state when routed through SHMRY self-awareness."""

    if any(x in q for x in ["last mutation", "last change", "last modified", "recent mutation", "latest mutation", "summarize your latest mutation", "what changed in your code today", "code today", "changed today"]):
        cmd = f"find {home} -type f \\( -name '*.py' -o -name '*.sh' -o -name '*.json' -o -name '*.db' -o -name '*.txt' \\) -printf '%T@ %TY-%Tm-%Td %TH:%TM %p\\n' 2>/dev/null | sort -nr | head -10"
        out = run(cmd, timeout=10)
        return f"""🧬 Last SHMRY/System Mutations Detected

Most recently modified relevant files:

{out or 'No recent files found.'}

Note: this is based on filesystem modification time, not biological mutation."""

    if any(x in q for x in ["largest file", "biggest file", "large file"]):
        cmd = f"find {home} -type f -printf '%s %p\\n' 2>/dev/null | sort -nr | head -10 | awk '{{size=$1; $1=\"\"; printf \"%.2f MB %s\\n\", size/1024/1024, $0}}'"
        out = run(cmd, timeout=15)
        return f"""📦 Largest Files I Can See

{out or 'Could not scan files.'}

This is from the local Linux filesystem under your home directory."""



    if any(x in q for x in ["most used file", "most accessed file", "recently used file"]):
        out = run(f"find {home} -type f -printf '%A@ %p\n' 2>/dev/null | sort -nr | head -15", timeout=12)
        return f"""📌 Most Recently Used Files

{out or 'Could not read file access times.'}

Note: Linux access time may be approximate depending on filesystem settings."""

    if any(x in q for x in ["state of art file", "state-of-art file", "most important file", "core file", "primary file"]):
        return f"""🏛️ SHMRY Core / State Files

Primary runtime:
{home}/shmry_ai_executor.py

Primary memory:
{home}/shmry_core/memory/memory.db

Largest active knowledge/database store:
{home}/shmry_cloud_hyperscale/vault/shmry_cloud.db

Main high-capability environment:
{home}/shmry_10of10/venv

Meaning:
These are not neural-network weights. They are SHMRY's local agent runtime, memory, data, and tool environment."""


    if any(x in q for x in [
        "how many versions of shmry",
        "how many executors",
        "executor versions",
        "version sprawl",
        "how many backups"
    ]):
        versions = run(f"find {home} -maxdepth 1 -type f -name 'shmry_ai_executor*' | wc -l")
        files = run(f"find {home} -maxdepth 1 -type f -name 'shmry_ai_executor*' | sort | tail -40", timeout=10)

        return f"""📚 SHMRY Version Inventory

Executor/backup files found:
{versions or '0'}

Recent executor files:
{files or 'None'}

Risk:
Large numbers of executor backups increase the chance of patching the wrong version.

Recommendation:
Keep one active executor, one stable backup, and archive the rest."""

    if any(x in q for x in ["do you learn and mutate", "can you learn and mutate", "learn and mutate", "do you mutate", "do you learn"]):
        mem = run(f"sqlite3 {home}/shmry_core/memory/memory.db \"select ts,kind,content,source from events order by id desc limit 1;\"", timeout=5)
        latest = run(f"find {home} -type f \\( -name '*.py' -o -name '*.sh' -o -name '*.db' -o -name '*.json' \\) -printf '%TY-%Tm-%Td %TH:%TM %p\n' 2>/dev/null | sort -r | head -5", timeout=10)
        return f"""🧬 Do I Learn and Mutate?

Yes — as SHMRY local agent, not as biological DNA and not as base-model retraining.

Learning evidence:
{mem or 'No memory event found.'}

Mutation evidence:
{latest or 'No recent mutation files found.'}

Meaning:
- Learning = storing/querying local memories and databases
- Mutation = code/config/plugin/file changes on your Linux system
- Base LLM weights are not being retrained here"""



    if any(x in q for x in ["most used file", "most accessed file", "recently used file"]):
        out = run(f"find {home} -type f -printf '%A@ %p\n' 2>/dev/null | sort -nr | head -15", timeout=12)
        return f"""📌 Most Recently Used Files

{out or 'Could not read file access times.'}

Note: Linux access time may be approximate depending on filesystem settings."""

    if any(x in q for x in ["state of art file", "state-of-art file", "most important file", "core file", "primary file"]):
        return f"""🏛️ SHMRY Core / State Files

Primary runtime:
{home}/shmry_ai_executor.py

Primary memory:
{home}/shmry_core/memory/memory.db

Largest active knowledge/database store:
{home}/shmry_cloud_hyperscale/vault/shmry_cloud.db

Main high-capability environment:
{home}/shmry_10of10/venv

Meaning:
These are not neural-network weights. They are SHMRY's local agent runtime, memory, data, and tool environment."""


    if any(x in q for x in [
        "how many versions of shmry",
        "how many executors",
        "executor versions",
        "version sprawl",
        "how many backups"
    ]):
        versions = run(f"find {home} -maxdepth 1 -type f -name 'shmry_ai_executor*' | wc -l")
        files = run(f"find {home} -maxdepth 1 -type f -name 'shmry_ai_executor*' | sort | tail -40", timeout=10)

        return f"""📚 SHMRY Version Inventory

Executor/backup files found:
{versions or '0'}

Recent executor files:
{files or 'None'}

Risk:
Large numbers of executor backups increase the chance of patching the wrong version.

Recommendation:
Keep one active executor, one stable backup, and archive the rest."""

    if any(x in q for x in ["do you learn and mutate", "can you learn and mutate", "learn and mutate", "do you mutate", "do you learn"]):
        mem = run(f"sqlite3 {home}/shmry_core/memory/memory.db \"select ts,kind,content,source from events order by id desc limit 1;\"", timeout=5)
        latest = run(f"find {home} -type f \\( -name '*.py' -o -name '*.sh' -o -name '*.db' -o -name '*.json' \\) -printf '%TY-%Tm-%Td %TH:%TM %p\n' 2>/dev/null | sort -r | head -5", timeout=10)
        return f"""🧬 Do I Learn and Mutate?

Yes — as SHMRY local agent, not as biological DNA and not as base-model retraining.

Learning evidence:
{mem or 'No memory event found.'}

Mutation evidence:
{latest or 'No recent mutation files found.'}

Meaning:
- Learning = storing/querying local memories and databases
- Mutation = code/config/plugin/file changes on your Linux system
- Base LLM weights are not being retrained here"""


    if any(x in q for x in ["what memory did you last store", "last memory", "last stored memory", "latest memory"]):
        dbs = run(f"find {home} -type f -name '*.db' | grep -Ei 'memory|semantic' | head -20", timeout=8)
        details = ""
        for db in dbs.splitlines():
            tables = run(f"sqlite3 '{db}' '.tables'", timeout=4)
            details += f"\nDB: {db}\nTables: {tables}\n"
            for table in tables.split():
                rows = run(f"sqlite3 '{db}' \"select * from {table} order by rowid desc limit 3;\"", timeout=4)
                if rows:
                    details += f"Latest rows from {table}:\n{rows}\n"
        return f"""🧠 Latest Stored Memory

{details or 'No readable memory database rows found.'}

This is based on local SQLite memory databases under your home directory."""

    if any(x in q for x in ["biggest risks", "largest risks", "your risks", "risk report", "top risks"]):
        disk = run("df -h $HOME | tail -1 | awk '{print $5\" used on \"$6}'")
        pyerrs = run(f"python3 -m py_compile {home}/shmry_ai_executor.py 2>&1 || true", timeout=8)
        backups = run(f"find {home} -maxdepth 2 -type f \\( -name '*.bak' -o -name '*.tar.gz' \\) | wc -l")
        secrets = run(f"grep -RIl --exclude-dir=venv --exclude-dir=.git -Ei 'api_key|secret|token|password' {home}/shmry* 2>/dev/null | head -10", timeout=10)
        return f"""⚠️ SHMRY Risk Report

Top risks detected:
1. Disk pressure: {disk or 'unknown'}
2. Syntax health: {'OK' if not pyerrs else pyerrs}
3. Backup/archive sprawl: {backups or 'unknown'} backup-like files found near home.
4. Secret exposure risk files:
{secrets or 'No obvious secret files found in shallow SHMRY scan.'}

Recommended:
- Keep disk below 80%
- Backup before every mutation
- Never commit API keys
- Add tests before auto-mutations
- Keep a rollback script ready"""

    if any(x in q for x in ["who are you", "what are you", "your capabilities", "what can you do"]):
        return """I am SHMRY running as a local AI agent wrapper.

Current capability layers may include:
- LLM answering
- Local filesystem inspection
- Memory modules
- Finance/backtest tools
- Steel analyzer plugin
- Cash wallet prototype
- Bash/Python automation

For exact status, ask:
- shmry how are you?
- shmry what was last mutation in you?
- shmry what is your largest file?"""

    return None
# ==== END SHMRY SELF-AWARENESS PREEMPT v1 ====


#!/usr/bin/env python3
import sys
import os
from datetime import datetime
from google import genai

# Setup
API_KEY = os.getenv("GOOGLE_API_KEY") or os.getenv("GEMINI_API_KEY")
if not API_KEY:
    print("Error: GOOGLE_API_KEY or GEMINI_API_KEY not set.")
    sys.exit(1)

client = genai.Client(api_key=API_KEY)

def time_logic(q):
    now = datetime.now()
    return f"Current time in Islamabad: {now.strftime('%A, %B %d, %Y %H:%M:%S')} PKT."

def llm_bridge(q):
    pre = __shmry_self_awareness_preempt(q if 'q' in locals() else (query if 'query' in locals() else ''))
    if pre:
        return pre
    try:
        sys_context = f"Current date/time: {datetime.now().isoformat()}. Answer accurately and concisely: "
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=[sys_context + q]
        )
        return response.text.strip()
    except Exception as e:
        return f"LLM Error: {str(e)}"

def run(query):
    q = query.lower().strip()
    if "time" in q or "date" in q:
        return time_logic(q)
    if "backup" in q:
        return "cp -a ~/shmry_ai_executor.py ~/shmry_ai_executor.bak"
    if any(k in q for k in ["steel", "math", "profit"]):
        return "Steel Math: Profit PKR 32,500/ton."
    return llm_bridge(query)

if __name__ == "__main__":
    if len(sys.argv) > 1:
        print(run(" ".join(sys.argv[1:])))
    else:
        print("Usage: shmry <your query>")
