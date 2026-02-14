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
    Use `reliability-engineer` skill (from Batch 2) to audit performance.
3.  **Docs**:
    ```bash
    python .agent/skills/readme-generator/scripts/readme_gen.py --name "My App" > README.md
    ```

### Step 4: Quick Deploy (Cloudflare Tunnel)
If user needs to share/demo their local site without hosting or domain:
```bash
# Expose local dev server to the internet instantly
python .agent/skills/deployment-wizard/scripts/tunnel.py --port 3000

# Auto-install cloudflared if not found
python .agent/skills/deployment-wizard/scripts/tunnel.py --port 3000 --install
```
> Generates a public `*.trycloudflare.com` URL. No account, no config needed.
