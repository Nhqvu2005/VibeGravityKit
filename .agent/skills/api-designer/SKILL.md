---
name: api-designer
description: Designs standard RESTful API endpoints and exports to OpenAPI.
---

# API Designer

## Purpose
Generates RESTful API endpoints and OpenAPI (Swagger) specifications.

## Usage

### 1. Generate Endpoints (Text List)
```bash
python .agent/skills/api-designer/scripts/api_gen.py --resources "users, products"
```

### 2. Export OpenAPI Spec (Yaml)
Generate a `swagger.yaml` file ready for Swagger UI or Code Gen.
```bash
python .agent/skills/api-designer/scripts/api_gen.py --resources "users, products" --export openapi > docs/swagger.yaml
```
