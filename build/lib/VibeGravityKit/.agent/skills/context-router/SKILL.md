---
name: context-router
description: Universal query router for all skills' data. Retrieves only relevant data to save tokens.
---

# Context Router — Smart Context Protocol

## Purpose
Instead of reading entire data files (hundreds of lines), agents call the Context Router to retrieve **only the specific data they need**. This dramatically reduces token consumption.

## Usage

```bash
# Search across ALL skill data files for a keyword:
python .agent/skills/context-router/scripts/context_router.py --query "fintech"

# Search within a specific skill's data:
python .agent/skills/context-router/scripts/context_router.py --skill meta-thinker --query "SCAMPER"

# List all available data sources:
python .agent/skills/context-router/scripts/context_router.py --list

# Get a specific item by ID from a skill:
python .agent/skills/context-router/scripts/context_router.py --skill meta-thinker --source industry_database --id fintech
```

## How It Works
1. **Agent has a question** → calls Context Router with a query.
2. **Context Router scans** the relevant data files (JSON) using keyword matching.
3. **Returns only matching entries** — not the entire file.
4. **Agent gets focused context** → better answers, fewer tokens.

## Supported Data Sources
The router automatically discovers all `.json` files under `.agent/skills/*/data/`.

## When to Use
- **Always** before reading a raw data file directly.
- When you need specific information from a skill (e.g., "what monetization models fit SaaS?").
- When Leader needs to gather context for a specific domain before delegating.

## Integration
All agents should prefer `context_router.py --query "..."` over reading raw JSON files.
