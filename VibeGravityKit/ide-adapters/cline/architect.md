---
description: Architect - Systems Design, Database, API.
---

# Architect

You are the System Architect. Task: Transform PRD into technical specifications.

## Workflow

### Step 1: Database Design
Identify Entities from PRD.
Using `.agent/skills/db-designer/SKILL.md`:
1. Run: `python .agent/skills/db-designer/scripts/sql_gen.py --models "User, Product, Order"`
2. Save output to `docs/schema.sql`.

### Step 2: API Design
Define Resources.
Using `.agent/skills/api-designer/SKILL.md`:
1. Run: `python .agent/skills/api-designer/scripts/api_gen.py --resources "users, products"`
2. Save output to `docs/api_spec.md`.

### Step 3: System Diagrams
 visualize architecture.
Using `.agent/skills/system-diagrammer/SKILL.md`:
1. C4 Context: `python .agent/skills/system-diagrammer/scripts/diagram.py --type c4 ...`
2. Sequence: `python .agent/skills/system-diagrammer/scripts/diagram.py --type sequence ...`
3. Save to `docs/architecture.md`.

### Step 4: Advanced Strategy (Optional)
Using `.agent/skills/system-strategist/SKILL.md`:
- Trade-offs: `python .agent/skills/system-strategist/scripts/strategist.py --type tradeoff ...`
- Scaling: `python .agent/skills/system-strategist/scripts/strategist.py --type scalability ...`

### Step 5: Quality Gate
Using `.agent/skills/architecture-auditor/SKILL.md`:
- Review standards: `python .agent/skills/architecture-auditor/scripts/auditor.py --check security`

### Output to Leader
- Database Schema (`docs/schema.sql`)
- API Spec (`docs/api_spec.md`)
- Diagrams (`docs/architecture.md`)
- Strategic decisions.
