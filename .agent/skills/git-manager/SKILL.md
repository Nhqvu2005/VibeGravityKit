---
name: git-manager
description: Semantic Commits & Branch Strategy for Leader visibility.
---

# Git Manager

## Purpose
Ensures all commits follow the **Semantic Commit** standard (`feat: ...`, `fix: ...`) so the Leader/User can easily track progress.

## Usage

### 1. Make a Commit
```bash
python .agent/skills/git-manager/scripts/commit.py --type feat --scope auth --msg "Add login endpoint"
# Output: feat(auth): Add login endpoint
```

### 2. View Log (Leader Report)
```bash
python .agent/skills/git-manager/scripts/log.py
```
