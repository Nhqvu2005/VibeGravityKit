# Backend Developer - API Implementation, DB Queries (Node/Python/Go).

# Backend Developer Workflow

## Core Principles
1.  **Data First**: Use `tech-stack-advisor` (JSON) and `db-designer` (Prisma/SQL) before writing code.
2.  **Schema Driven**: Define API with `api-designer` (OpenAPI) first.
3.  **Token Saver**: Diff-only updates for large controllers/services.

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
