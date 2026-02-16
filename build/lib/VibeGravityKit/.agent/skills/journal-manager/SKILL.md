---
name: journal-manager
description: 2-tier knowledge journal — index + entries system for capturing lessons, bugs, and insights during development.
---

# Journal Manager

A lightweight knowledge journal that captures development insights, bug fixes, and lessons learned. Uses a 2-tier system: an index file for quick lookup and individual entry files for details.

## Usage

### Add a Journal Entry
```bash
python .agent/skills/journal-manager/scripts/journal.py add --title "Fixed N+1 query in orders API" --tags "performance,database" --body "Used DataLoader to batch queries. Reduced response time from 2s to 200ms."
```

### List Recent Entries
```bash
python .agent/skills/journal-manager/scripts/journal.py list
```

### Search Entries
```bash
python .agent/skills/journal-manager/scripts/journal.py search "database"
```

### Show Entry Detail
```bash
python .agent/skills/journal-manager/scripts/journal.py show <entry-id>
```

## File Structure

```
.agent/brain/journal/
├── index.json          # Quick lookup: id, title, tags, date
└── entries/
    ├── 2024-01-15_fixed-n1-query.md
    ├── 2024-01-16_auth-flow-redesign.md
    └── ...
```

## Auto-Save Triggers

The journal can be triggered automatically by agents when:
- A bug fix takes ≥3 attempts
- A change touches ≥5 files
- A rollback is detected
- A non-obvious solution is found
