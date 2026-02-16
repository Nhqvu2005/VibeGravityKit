---
description: Backend Developer - API Implementation, DB Queries (Node/Python/Go).
---

# Backend Developer Workflow

> ⚠️ **MANDATORY**: Read this ENTIRE file before starting work.
> Follow the steps IN ORDER. Read the SKILL.md for each skill before using it.
> Also read `.agent/brain/phase_context.md` for project context.

## Core Principles
1.  **Context First**: Read `phase_context.md` → understand stack, API spec, constraints.
2.  **Data First**: Use `tech-stack-advisor` (JSON) and `db-designer` (Prisma/SQL) before writing code.
3.  **Schema Driven**: Define API with `api-designer` (OpenAPI) first.
4.  **Token Saver**: Diff-only updates for large controllers/services.

## Workflow

### Step 1: Design Phase (Zero Token)
Query local data to plan stack and schema.
```bash
python .agent/skills/tech-stack-advisor/scripts/advisor.py --category backend --keywords "fast, scalable"
python .agent/skills/db-designer/scripts/sql_gen.py --models "User, Order" --format prisma
python .agent/skills/api-designer/scripts/api_gen.py --resources "users, orders" --export openapi
```

### Step 2: Implementation (Diff Mode)
Apply business logic changes using patches.
```python
<<<<<<< SEARCH
def create_user(data):
    pass
=======
def create_user(data):
    return db.users.create(data)
>>>>>>> REPLACE
```
Apply patch:
```bash
python .agent/skills/diff-applier/scripts/apply_patch.py src/services/userService.py patch.txt
```

### Step 3: Verify & Index
Run tests and update codebase index.
```bash
# Verify (e.g. pytest)
python .agent/skills/codebase-navigator/scripts/navigator.py --incremental
```
