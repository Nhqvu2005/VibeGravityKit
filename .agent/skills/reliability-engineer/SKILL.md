---
name: reliability-engineer
description: Observability, Incident Management & Performance Optimization (SRE).
---

# Reliability Engineer (SRE)

## Purpose
Ensures stable system operation, easy monitoring (Observability), and effective incident response. Integrates Performance Optimization functions.

## Usage

### 1. Observability Design
Propose monitoring stack (Metrics, Logs, Tracing).
```bash
python .agent/skills/reliability-engineer/scripts/sre.py --action observability
```

### 2. Incident Report (RCA)
Create incident report template for Root Cause Analysis.
```bash
python .agent/skills/reliability-engineer/scripts/sre.py --action incident --title "Database High Latency"
```

### 3. Performance Tuning
Suggest performance optimizations for each layer.
```bash
python .agent/skills/reliability-engineer/scripts/sre.py --action performance --area database
```
*Areas: database, backend, frontend*
