---
name: tech-stack-advisor
description: Suggests suitable tech stack based on project requirements using local database.
---

# Tech Stack Advisor

## Purpose
Recommends the best Technology Stack (Frontend, Backend, Database) based on constraints (SEO, Performance, Speed).
Also supports scanning legacy codebases.

## Usage

### 1. New Project Advice
```bash
python .agent/skills/tech-stack-advisor/scripts/advisor.py --category web --keywords "seo,fast"
```

### 2. Legacy Project Scan
Identify stack of existing code.
```bash
python .agent/skills/tech-stack-advisor/scripts/scanner.py --path "."
```

### 3. Compare Stacks
Compare Pros/Cons of different choices.
```bash
python .agent/skills/tech-stack-advisor/scripts/advisor.py --compare --category web
```
