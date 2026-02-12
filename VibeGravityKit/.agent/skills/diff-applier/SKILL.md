---
name: diff-applier
description: Smart Patcher — Apply Diff, Lint, and Auto-Index.
---

# Diff Applier

## Purpose
Apply code changes ("patches") safely, saving tokens by not rewriting the whole file. Automatically checks for lint errors and updates the codebase index.

## Usage

### 1. Create a Patch File
The patch file must use `SEARCH/REPLACE` blocks:
```text
<<<<<<< SEARCH
def old_function():
    return True
=======
def new_function():
    return False
>>>>>>> REPLACE
```

### 2. Apply Patch
```bash
python .agent/skills/diff-applier/scripts/apply_patch.py src/main.py my_patch.txt
```

## Workflow
1.  **Backup**: Creates `src/main.py.bak`.
2.  **Apply**: Replaces exact text matches.
3.  **Lint**: Runs `flake8` (Python) or `eslint` (JS) if available.
4.  **Index**: Calls `codebase-navigator` to update the project index.
