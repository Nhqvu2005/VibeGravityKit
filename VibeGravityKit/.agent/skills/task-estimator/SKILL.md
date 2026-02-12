---
name: task-estimator
description: Breaks down features into tasks, assigns roles, and estimates effort/timeline.
---

# Task Estimator

## Purpose
Helps Planner break down high-level features into estimable development tasks.

## Usage

### 1. Estimate Feature
```bash
python .agent/skills/task-estimator/scripts/estimator.py --feature "User Authentication"
```

### Output
- Breakdown: Database Schema, API Endpoint, UI Login Page, UI Register Page.
- Role: Backend, Frontend, Designer.
- Effort: Hours/Points per task.
- Total estimated time.
