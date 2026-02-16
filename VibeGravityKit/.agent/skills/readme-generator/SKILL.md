---
name: readme-generator
description: Auto-generate concise, visually stunning README.md with project auto-scanning, badges, and 3 style modes.
---

# README Generator v2

## Purpose
Generate **concise, scannable** README files that look premium on GitHub. Auto-detects project context and generates badges, features, and install instructions.

## Design Philosophy
- **Scan, don't read** — Tables, badges, one-liners over paragraphs
- **Visual-first** — Center-aligned hero, shields.io badges, emoji headings
- **No walls of text** — Max 2-3 sentences per section, use tables/bullets
- **Smart detection** — Auto-reads `package.json`, `setup.py`, `VERSION`, `.agent/` to fill real data

## Usage

### Auto-generate (recommended)
```bash
# Scan project and generate README
python .agent/skills/readme-generator/scripts/readme_gen.py --path .

# With specific style
python .agent/skills/readme-generator/scripts/readme_gen.py --path . --style minimal
python .agent/skills/readme-generator/scripts/readme_gen.py --path . --style standard   # default
python .agent/skills/readme-generator/scripts/readme_gen.py --path . --style detailed
```

### Custom fields
```bash
python .agent/skills/readme-generator/scripts/readme_gen.py \
  --path . \
  --name "My Project" \
  --slogan "One line that sells" \
  --author "username" \
  --image "https://example.com/banner.png"
```

## Style Modes

| Mode | Lines | Best For |
|------|-------|----------|
| `minimal` | ~40-60 | Libraries, packages, simple tools |
| `standard` | ~80-120 | Most projects (default) |
| `detailed` | ~120-180 | Complex frameworks, multi-component projects |

## What It Auto-Detects
| Source | Extracts |
|--------|----------|
| `package.json` | Name, version, license, scripts, dependencies |
| `setup.py` / `pyproject.toml` | Name, version, license, dependencies |
| `VERSION` | Version number |
| `LICENSE` | License type |
| `.agent/skills/` | Skill count |
| `.agent/workflows/` | Workflow/agent count |
| `Dockerfile` | Docker support |
| `tsconfig.json` | TypeScript detection |

## Key Rules for Agent
1. **Never write paragraphs** — Use tables, bullets, or one-liners
2. **Hero must be centered** — `<div align="center">` with title + badges + image
3. **Features in tables** — `| Emoji Feature | One-line description |`
4. **Install in ≤ 5 lines** — Clone → install → run, no prose
5. **Only relevant sections** — Skip Docker section if no Dockerfile
