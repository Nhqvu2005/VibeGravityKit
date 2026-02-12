---
name: db-designer
description: Generates standard SQL or Prisma database schemas.
---

# Database Designer

## Purpose
Generates database schemas for common entities in SQL or Prisma format.

## Usage

### 1. Generate SQL
```bash
python .agent/skills/db-designer/scripts/sql_gen.py --models "User, Product" --format sql
```

### 2. Generate Prisma Schema
Generate `schema.prisma` models for modern Node.js stacks (Next.js, NestJS).
```bash
python .agent/skills/db-designer/scripts/sql_gen.py --models "User, Product" --format prisma
```
