# Deploy Recipe — Compact Agent Prompt

> Read this ONLY when user asks to deploy/share/publish locally.
> This replaces reading the full devops.md deploy section.

## 3-Step Deploy

### Step 1: Find free port + get serve command
```bash
python .agent/skills/deployment-wizard/scripts/tunnel.py --find-port --serve-cmd {{STACK}} --quiet
```
Output: `FREE_PORT=XXXX` and `SERVE_CMD=...`

Replace `{{STACK}}` with: `static` | `react` | `vite` | `nextjs` | `nuxt` | `django` | `flask` | `fastapi` | `express` | `php` | `hugo` | `ruby`

If unsure which stack → check `package.json` or project files to detect.

### Step 2: Start server (background)
Run the `SERVE_CMD` from Step 1 (replace `{{PORT}}` with `FREE_PORT`).

### Step 3: Start tunnel (background)
```bash
python .agent/skills/deployment-wizard/scripts/tunnel.py --port XXXX --quiet
```
Wait 10-15s → parse `TUNNEL_URL=https://...` → return to user.

## Quick Ref
| Output | Meaning |
|--------|---------|
| `FREE_PORT=XXXX` | Use this port |
| `SERVE_CMD=...` | Run this to start server |
| `TUNNEL_URL=https://...` | Share this URL |
| `ERROR=...` | Report to user |
