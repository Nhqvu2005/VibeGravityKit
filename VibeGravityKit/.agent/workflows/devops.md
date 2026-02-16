---
description: DevOps Engineer - Docker, CI/CD, Cloud Deployment.
---

# DevOps Engineer Workflow

> ⚠️ **MANDATORY**: Read this ENTIRE file before starting work.
> Follow the steps IN ORDER. Read the SKILL.md for each skill before using it.
> Also read `.agent/brain/phase_context.md` for project context.

## Core Principles
1.  **Automation First**: If you do it twice, script it (or use `docker-wizard`/`ci-cd-setup`).
2.  **Infrastructure as Code**: Everything in Git.
3.  **Token Saver**: Use `context-manager` when debugging logs.

## Workflow

### Step 1: Containerization (Zero Token)
```bash
python .agent/skills/docker-wizard/scripts/docker_gen.py --stack node --db postgres
```

### Step 2: CI/CD Pipeline (Zero Token)
```bash
python .agent/skills/ci-cd-setup/scripts/ci_gen.py --type node --platform github
```

### Step 3: Monitoring & Release
1.  **Tag Release**:
    ```bash
    python .agent/skills/git-manager/scripts/commit.py --type build --msg "Bump version"
    git tag v1.0.0
    ```
2.  **Check Health**: Use `reliability-engineer` skill.
3.  **Docs**: `python .agent/skills/readme-generator/scripts/readme_gen.py --name "App" > README.md`

### Step 4: Quick Deploy (Cloudflare Tunnel)
When user wants to deploy/share/publish locally:
📖 **Read** `.agent/skills/deployment-wizard/data/deploy_recipe.md` for full instructions.
