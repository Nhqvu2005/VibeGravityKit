---
name: strategic-planning-advisor
description: Advises on system architecture, scalability, and long-term maintenance strategy.
---

# Strategic Planning Advisor

## Purpose
High-level architectural advice for the Leader. Focuses on "Big Picture" decisions before writing code.

## Usage

### 1. Get Advice
```bash
python .agent/skills/strategic-planning-advisor/scripts/strategy.py --query "high traffic e-commerce"
```

### Logic
- Analyzes requirements (Traffic, Complexity, Budget).
- Recommends Architecture (Monolith vs Microservices).
- Suggests Database strategy (SQL vs NoSQL).
- Estimates Infrastructure costs (Low/Medium/High).
