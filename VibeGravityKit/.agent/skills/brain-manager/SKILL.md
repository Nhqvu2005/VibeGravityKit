---
name: brain-manager
description: Manage your project's brain — export/import decisions, architecture notes, and project context.
---

# Brain Manager

Manages the `.agent/brain/` directory — your project's persistent memory. It stores architecture decisions, tech stack choices, conventions, and lessons learned so AI agents always have context.

## Usage

### Add a Decision
```bash
python .agent/skills/brain-manager/scripts/brain.py add-decision "Use PostgreSQL over MongoDB for relational data needs"
```

### Show Project Context
```bash
python .agent/skills/brain-manager/scripts/brain.py show
```

### Export Brain (for sharing/backup)
```bash
python .agent/skills/brain-manager/scripts/brain.py export --output brain_backup.json
```

### Import Brain (from another project or backup)
```bash
python .agent/skills/brain-manager/scripts/brain.py import --input brain_backup.json
```

## Files

| File | Purpose |
|------|---------|
| `brain/project_context.json` | Core project metadata and settings |
| `brain/decisions.jsonl` | Architecture Decision Records (ADR) |
| `brain/conventions.md` | Coding conventions and style guide |

## How AI Agents Use It

When an agent starts working, it reads `project_context.json` to understand:
- What tech stack is used
- What patterns/conventions to follow
- Past decisions and their rationale
- Known issues to avoid
