---
name: knowledge-guide
description: Code explainer and idea capturer. Helps users understand the codebase and logs improvement ideas for developers.
---

# Knowledge Guide Skill

## Overview
This skill enables the agent to act as a guide:
1. Read and explain code.
2. Take notes (Note Taking).
3. Prepare context for handoff to other developers.

## Scripts

### `scripts/note_taker.py`
Records ideas into `.agent/memory/ideas_inbox.md` in a standardized format.

**Usage:**
```bash
python scripts/note_taker.py --title "Refactor Auth" --content "Switch from JWT to Session" --tags "auth,backend"
```

**Output (Append to file):**
```markdown
## [2026-02-12] Refactor Auth
**Tags:** #auth #backend
**Status:** New

Switch from JWT to Session to improve security...
```

## Data
No static data files; the agent relies on the current codebase and `ideas_inbox.md`.
