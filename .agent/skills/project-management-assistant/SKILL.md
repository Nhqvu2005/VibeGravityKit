---
name: project-management-assistant
description: Assists Planner in managing scope, risks, and milestone planning.
---

# Project Management Assistant

## Purpose
Helps Planner define realistic scope (MVP), identify risks early, and plan milestones based on team capacity.

## Usage

### 1. Scope Check (MVP Definition)
Validate if features fit into the timeline.
```bash
python .agent/skills/project-management-assistant/scripts/pm_assistant.py --action scope --features "Auth, Search, Payment, Admin" --weeks 4
```

### 2. Risk Assessment
Identify potential risks based on keywords.
```bash
python .agent/skills/project-management-assistant/scripts/pm_assistant.py --action risk --keywords "payment gateway, ai integration"
```

### 3. Milestone Planning
Generate a week-by-week plan.
```bash
python .agent/skills/project-management-assistant/scripts/pm_assistant.py --action plan --weeks 8
```
