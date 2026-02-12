---
name: progress-tracker
description: Tracks project progress, creates status reports for Manager.
---

# Progress Tracker

## Purpose
Parses `task.md` or git status to generate professional status reports for the Manager/User.

## Usage

### 1. Generate Report
```bash
python .agent/skills/progress-tracker/scripts/tracker.py --source task.md
```

### Output
- Completed Tasks %.
- Current Bottlenecks.
- Next Steps.
- Formatted Markdown report.
