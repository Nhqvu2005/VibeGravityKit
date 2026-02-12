---
name: system-strategist
description: High-level decision maker for Trade-offs, Scalability & Migration Strategy.
---

# System Strategist

## Purpose
Assists Architect in making difficult decisions (Trade-offs), planning for growth (Scalability), and system transition strategies (Migration).

## Usage

### 1. Tradeoff Evaluator
Compare technical choices (SQL vs NoSQL, Monolith vs Microservices...).
```bash
python .agent/skills/system-strategist/scripts/strategist.py --type tradeoff --topic "sql_vs_nosql"
```

### 2. Scalability Planner
Propose infrastructure solutions based on expected user count.
```bash
python .agent/skills/system-strategist/scripts/strategist.py --type scalability --users 100000
```
*Output: Caching, Read Replicas, Worker Queues...*

### 3. Migration Strategist
Choose safe deployment or migration strategies (Strangler Fig, Blue-Green, Canary).
```bash
python .agent/skills/system-strategist/scripts/strategist.py --type migration --strategy "strangler_fig"
```

## Supported Topics
- **Trade-offs**: `sql_vs_nosql`, `monolith_vs_microservices`, `rest_vs_graphql`
- **Scalability**: 10k, 100k, 1M+ users logic
- **Migration**: `strangler_fig`, `blue_green`, `canary`
