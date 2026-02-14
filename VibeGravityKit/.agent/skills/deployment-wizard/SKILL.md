---
name: deployment-wizard
description: Deploy local websites to the internet instantly via Cloudflare Tunnel. Zero hosting, zero domain needed.
---

# Deployment Wizard

## Purpose
Expose any local website/server to the internet using **Cloudflare Tunnel** (cloudflared).
Perfect for demos, testing, sharing local dev servers — without hosting or domain.

## How It Works
1. Auto-downloads `cloudflared` binary (if not installed)
2. Creates a temporary **Quick Tunnel** to your local port
3. Generates a public `*.trycloudflare.com` URL
4. **No Cloudflare account needed. No API key. No config.**

## Usage

### Human Mode (interactive UI)
```bash
python .agent/skills/deployment-wizard/scripts/tunnel.py --find-port
# ✅ Free port found: 3000

python .agent/skills/deployment-wizard/scripts/tunnel.py --port 3000
python .agent/skills/deployment-wizard/scripts/tunnel.py --check
```

### Agent Mode (--quiet, machine-parseable output)
```bash
# STEP 1: Pre-flight — find a free port (ALWAYS do this first!)
python .agent/skills/deployment-wizard/scripts/tunnel.py --find-port --quiet
# → FREE_PORT=3000

# STEP 2: Start your server on that port
# (your server command here, using the FREE_PORT from step 1)

# STEP 3: Start tunnel on that port
python .agent/skills/deployment-wizard/scripts/tunnel.py --port 3000 --quiet
# → TUNNEL_URL=https://xxx.trycloudflare.com
```

### Port Safety
> ⚠️ **NEVER start a server or tunnel on a port without checking first.**

The `--find-port` command scans ports 3000-9999 and returns the first free one.
Use `--start <N>` to search from a specific port: `--find-port --start 5000`

### Agent Automation Steps (mandatory order)
1. `--find-port --quiet` → get `FREE_PORT=XXXX` (do this BEFORE anything else)
2. `--check --quiet` → verify cloudflared installed
3. Start local server on `XXXX` (the free port from step 1)
4. `--port XXXX --quiet` → start tunnel (background command)
5. Parse `TUNNEL_URL=` from output → return to user

### Output Format (--quiet)
| Output | Meaning |
|--------|---------|
| `FREE_PORT=XXXX` | Pre-flight: free port found |
| `STATUS=installed` | cloudflared found |
| `STATUS=not_installed` | Need to install |
| `INSTALLED=/path` | Just installed |
| `TUNNEL_URL=https://...` | Tunnel is live! |
| `ERROR=port_busy` | Port is occupied |
| `ERROR=message` | Something failed |

### Common Ports
| Stack | Default Port | Note |
|-------|-------------|------|
| React (Vite) | 5173 | Always use --find-port first |
| Next.js | 3000 | May conflict with other Node apps |
| Django | 8000 | Often used by other services |
| Flask | 5000 | macOS AirPlay uses 5000 |

## Requirements
- Python 3.9+ (stdlib only — zero pip dependencies)
- Internet connection
- Local server running on the specified port
