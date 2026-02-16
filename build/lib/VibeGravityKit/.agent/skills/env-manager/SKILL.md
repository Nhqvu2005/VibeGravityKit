---
name: env-manager
description: Auto-generate .env.example from your codebase. Scans for environment variable usage and creates a safe template.
---

# Env Manager

Scans your project for environment variable references and generates a `.env.example` file with all required variables documented.

## Usage

Run the script to scan your project:

```bash
python .agent/skills/env-manager/scripts/env_scanner.py --path "."
```

### Output

Generates `.env.example` with:
- All detected environment variables
- Grouped by source file
- Placeholder values and descriptions

## Data

- `data/common_env_vars.json` — Common env var patterns and safe defaults

## Notes

- Never copies actual secret values
- Supports `.env`, `process.env`, `os.environ`, `os.getenv` patterns
- Groups variables by category (DB, Auth, API, etc.)
