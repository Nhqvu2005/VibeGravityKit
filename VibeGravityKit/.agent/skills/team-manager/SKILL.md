---
name: team-manager
description: Persistent team profiles — carry your coding style, rules, and bug-fix knowledge across projects. 3-tier memory (Hot/Warm/Cold) with TF-IDF search.
---

# Team Manager

Persistent team profiles stored globally (`~/.vibegravity/teams/`). When you init a project with `--team`, your coding style (DNA), rules, and journal entries auto-inject into the project.

## 3-Tier Memory

- **🔴 Hot** (~50 tokens) — Team DNA (1 line) + top rules. Always loaded.
- **🟡 Warm** (~200 tokens) — Full rules + journal index. Searched on demand via TF-IDF.
- **🔵 Cold** (0 tokens) — Archive. Only loaded manually.

## Usage

### Create a Team (scans existing project)
```bash
python .agent/skills/team-manager/scripts/team_manager.py create my-team --scan ./old-project
```

### Init Project with Team
```bash
vibegravity init antigravity --team my-team
```

### Add Rules
```bash
python .agent/skills/team-manager/scripts/team_manager.py rule add "Always write docs in English"
python .agent/skills/team-manager/scripts/team_manager.py rule add "Use Tailwind" --agent frontend-dev
```

### Sync Teams
```bash
python .agent/skills/team-manager/scripts/team_manager.py sync other-team
```

### Export / Import
```bash
python .agent/skills/team-manager/scripts/team_manager.py export my-team
python .agent/skills/team-manager/scripts/team_manager.py import team-my-team.zip
```

## For Agents

If `.agent/brain/team_dna.txt` exists, read it before writing any code. It contains the user's preferred style in compact format.

If `.agent/brain/team_rules/` exists, read your agent-specific file (e.g. `frontend.md`) for targeted rules.
