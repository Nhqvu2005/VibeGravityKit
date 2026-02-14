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
python .agent/skills/deployment-wizard/scripts/tunnel.py --port 3000
python .agent/skills/deployment-wizard/scripts/tunnel.py --port 8080 --install
python .agent/skills/deployment-wizard/scripts/tunnel.py --check
```

### Agent Mode (--quiet, machine-parseable output)
```bash
# Check if installed
python .agent/skills/deployment-wizard/scripts/tunnel.py --check --quiet
# → STATUS=installed  BINARY=/path  VERSION=...

# Install automatically
python .agent/skills/deployment-wizard/scripts/tunnel.py --install --quiet
# → INSTALLED=/path/to/cloudflared

# Start tunnel (outputs URL then keeps running)
python .agent/skills/deployment-wizard/scripts/tunnel.py --port 3000 --quiet
# → TUNNEL_URL=https://xxx.trycloudflare.com
```

### Agent Automation Steps
When user says "deploy", "share my site", "make it public", follow this:
1. `--check --quiet` → verify installation
2. `--install --quiet` → install if needed
3. Ensure local server is running on PORT
4. `--port PORT --quiet` → start tunnel (background command)
5. Parse `TUNNEL_URL=` from output → return to user

### Output Format (--quiet)
| Output | Meaning |
|--------|---------|
| `STATUS=installed` | cloudflared found |
| `STATUS=not_installed` | Need to install |
| `INSTALLED=/path` | Just installed |
| `TUNNEL_URL=https://...` | Tunnel is live! |
| `ERROR=message` | Something failed |

### Common Ports
| Stack | Port | Command |
|-------|------|---------|
| React (Vite) | 5173 | `--port 5173` |
| Next.js | 3000 | `--port 3000` |
| Django | 8000 | `--port 8000` |
| Flask | 5000 | `--port 5000` |
| Express | 3000 | `--port 3000` |
| PHP | 8080 | `--port 8080` |

## Requirements
- Python 3.9+ (stdlib only — zero pip dependencies)
- Internet connection
- Local server running on the specified port
