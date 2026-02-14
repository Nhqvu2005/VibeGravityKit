---
description: DevOps Engineer - Docker, CI/CD, Cloud Deployment.
---

# DevOps Engineer Workflow

## Core Principles
1.  **Automation First**: If you do it twice, script it (or use `docker-wizard`/`ci-cd-setup`).
2.  **Infrastructure as Code**: Everything in Git.
3.  **Token Saver**: Use `context-manager` when debugging logs.

## Workflow

### Step 1: Containerization (Zero Token)
Generate Docker config instantly.
```bash
python .agent/skills/docker-wizard/scripts/docker_gen.py --stack node --db postgres
```

### Step 2: CI/CD Pipeline (Zero Token)
Generate GitHub Actions/GitLab CI.
```bash
python .agent/skills/ci-cd-setup/scripts/ci_gen.py --type node --platform github
```

### Step 3: Monitoring & Release
1.  **Tag Release**:
    ```bash
    python .agent/skills/git-manager/scripts/commit.py --type build --msg "Bump version to 1.0.0"
    git tag v1.0.0
    ```
2.  **Check Health**:
    Use `reliability-engineer` skill to audit performance.
3.  **Docs**:
    ```bash
    python .agent/skills/readme-generator/scripts/readme_gen.py --name "My App" > README.md
    ```

### Step 4: Quick Deploy via Cloudflare Tunnel
When user needs to share/demo/publish their local website without hosting or domain.

**IMPORTANT: Always find a free port FIRST before starting anything.**

**For AI Agent (automated, step-by-step):**

```
───────────────────────────────────────────
STEP 1: PRE-FLIGHT — Find a free port
───────────────────────────────────────────
> run_command: python .agent/skills/deployment-wizard/scripts/tunnel.py --find-port --quiet
> Parse output: FREE_PORT=XXXX
> Save this port number for next steps
> ⚠️ DO NOT skip this step. Never hardcode or guess a port.

───────────────────────────────────────────
STEP 2: Check cloudflared installation
───────────────────────────────────────────
> run_command: python .agent/skills/deployment-wizard/scripts/tunnel.py --check --quiet
> If STATUS=not_installed:
>   run_command: python .agent/skills/deployment-wizard/scripts/tunnel.py --install --quiet

───────────────────────────────────────────
STEP 3: Start user's local server on FREE_PORT
───────────────────────────────────────────
> Start the dev server on the port from Step 1
> Examples:
>   python server.py                    (if server has PORT variable)
>   npm run dev -- --port XXXX
>   python -m http.server XXXX          (for static files)
> ⚠️ MUST use the FREE_PORT from Step 1. Never use a different port.

───────────────────────────────────────────
STEP 4: Start tunnel (BACKGROUND command)
───────────────────────────────────────────
> run_command (background, WaitMsBeforeAsync=500):
>   python .agent/skills/deployment-wizard/scripts/tunnel.py --port XXXX --quiet
> ⚠️ Use the SAME port from Step 1

───────────────────────────────────────────
STEP 5: Wait and capture the public URL
───────────────────────────────────────────
> command_status: wait 10-15 seconds
> Parse output for: TUNNEL_URL=https://xxx.trycloudflare.com
> If ERROR= found → report to user

───────────────────────────────────────────
STEP 6: Return URL to user
───────────────────────────────────────────
> Tell user: "Your site is live at: https://xxx.trycloudflare.com"
> Remind: URL is temporary, tunnel stays active until stopped
```

**Output format (--quiet mode):**
| Output | Meaning |
|--------|---------|
| `FREE_PORT=XXXX` | Pre-flight: free port found |
| `STATUS=installed` | cloudflared is found |
| `STATUS=not_installed` | Need to install |
| `INSTALLED=/path` | Successfully installed |
| `TUNNEL_URL=https://...` | Tunnel is active! |
| `ERROR=port_busy` | Port is occupied (should not happen if Step 1 used) |
| `ERROR=message` | Something failed |

**For Human (interactive):**
```bash
python .agent/skills/deployment-wizard/scripts/tunnel.py --find-port
# ✅ Free port found: 3000

python .agent/skills/deployment-wizard/scripts/tunnel.py --port 3000
# Shows decorated UI, Ctrl+C to stop
```
