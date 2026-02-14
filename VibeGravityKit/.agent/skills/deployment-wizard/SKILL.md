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
4. Anyone can access your local site via that URL
5. **No Cloudflare account needed. No API key. No config.**

## Usage

### Deploy a local website
```bash
# Expose localhost:3000 to the internet
python .agent/skills/deployment-wizard/scripts/tunnel.py --port 3000

# Auto-install cloudflared if missing + start tunnel
python .agent/skills/deployment-wizard/scripts/tunnel.py --port 8080 --install
```

### Check installation
```bash
python .agent/skills/deployment-wizard/scripts/tunnel.py --check
```

### Common ports
| Stack | Default Port | Command |
|-------|-------------|---------|
| React (Vite) | 5173 | `--port 5173` |
| Next.js | 3000 | `--port 3000` |
| Django | 8000 | `--port 8000` |
| Flask | 5000 | `--port 5000` |
| Express | 3000 | `--port 3000` |
| PHP | 8080 | `--port 8080` |
| Hugo | 1313 | `--port 1313` |

## Requirements
- Python 3.9+ (stdlib only — zero pip dependencies)
- Internet connection
- Local server running on the specified port

## Output
A public URL like: `https://random-words.trycloudflare.com`
