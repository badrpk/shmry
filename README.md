# SHMRY

**Unified infrastructure telemetry, governance, and automation** for hyperscale / CPEC-style environments.

SHMRY is **not** Sophyane (AI agent OS) and **not** Huobz (AI language ecosystem).  
It is the **ops + marketplace + governance** layer.

## Download

```bash
git clone https://github.com/badrpk/shmry.git
cd shmry
```

## Layout

| Path | Role |
|------|------|
| `core/` | Kernel / runtime hooks |
| `dashboard/` | Ops dashboard server |
| `marketplace/` | Commercial marketplace services |
| `modules/` | Pluggable ops modules |
| `business_brain/` | Business automation |
| `config/` | Configuration |
| `tests/` | Tests |
| `bin/` | CLI helpers |

## Quick start

```bash
# Health API (no external deps)
python3 scripts/health_server.py
# → http://127.0.0.1:8787/health

# Dashboard (if dependencies available)
python3 dashboard/server.py
```

## Marketplace

```bash
cd marketplace
python3 -c "import marketplace"  # when installed as package
# or run service entrypoints listed in marketplace/
```

## Contribute

Public and open — **download, use, fork, improve**.  
See [CONTRIBUTING.md](CONTRIBUTING.md) · [COMMUNITY.md](COMMUNITY.md)

## License

Contributions welcome. Prefer MIT-compatible PRs without secrets.
