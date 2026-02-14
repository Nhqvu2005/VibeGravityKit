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

**For AI Agent (automated):**
Follow this exact sequence to deploy and return the public URL:

```
STEP 1: Check if cloudflared is installed
> run_command: python .agent/skills/deployment-wizard/scripts/tunnel.py --check --quiet
> Parse output for STATUS=installed or STATUS=not_installed

STEP 2: If not installed, install it
> run_command: python .agent/skills/deployment-wizard/scripts/tunnel.py --install --quiet
> Parse output for INSTALLED=/path/to/binary or ERROR=...

STEP 3: Make sure user's local server is running
> Check if user already has a dev server running (npm run dev, python manage.py runserver, etc.)
> If not, start it first on the appropriate port

STEP 4: Start the tunnel (run in BACKGROUND with WaitMsBeforeAsync=500)
> run_command: python .agent/skills/deployment-wizard/scripts/tunnel.py --port PORT --quiet
> This command runs FOREVER (keeps tunnel alive). Send to background.

STEP 5: Wait and read the tunnel output
> command_status: wait 10-15 seconds for the tunnel to connect
> Parse output for TUNNEL_URL=https://xxx.trycloudflare.com
> If ERROR= found, report to user

STEP 6: Return the URL to user
> Tell user: "Your site is live at: https://xxx.trycloudflare.com"
> Remind: URL is temporary, changes on restart, Ctrl+C to stop
```

**Output format (--quiet mode):**
| Output | Meaning |
|--------|---------|
| `STATUS=installed` | cloudflared is found |
| `STATUS=not_installed` | Need to install |
| `INSTALLED=/path/to/binary` | Successfully installed |
| `TUNNEL_URL=https://xxx.trycloudflare.com` | Tunnel is active! |
| `ERROR=message` | Something failed |

**For Human (interactive):**
```bash
python .agent/skills/deployment-wizard/scripts/tunnel.py --port 3000
# Shows decorated UI, Ctrl+C to stop
```
