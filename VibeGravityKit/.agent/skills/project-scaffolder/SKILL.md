---
name: project-scaffolder
description: Creates standard project structure with config files, linting, formatting.
---

# Project Scaffolder

## Purpose
Instantly sets up a professional project structure with best practices (Linters, Gitignore, Readme, Folder structure).

## Usage

### 1. Scaffold Project
```bash
python .agent/skills/project-scaffolder/scripts/scaffold.py --stack "nextjs" --name "my-app"
```

### Supported Stacks
- `nextjs`: Next.js + Tailwind + TypeScript
- `python-api`: FastAPI/Flask structure
- `mern`: Mongo, Express, React, Node
- `data-science`: Jupyter, Pandas, Scikit-learn structure
- `html-css-js`: Vanilla HTML + CSS + JS Structure

### Output
Generated folders and files in the current directory (or target directory).
