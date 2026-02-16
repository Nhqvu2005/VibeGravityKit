---
name: codebase-navigator
description: Index & Search code quickly (Token Saver) for legacy projects.
---

# Codebase Navigator

## Purpose
Helps Leader/Planner understand legacy project structure and helps Dev locate code without reading entire files (Huge token saver).

## Usage

### 1. Index Codebase (First run)
Scan entire project and map symbols (Functions, Classes).
```bash
python .agent/skills/codebase-navigator/scripts/navigator.py --action index --path "."
```

### 2. Project Map
List file structure and key functions/classes. Used by Leader for context.
```bash
python .agent/skills/codebase-navigator/scripts/navigator.py --action map
```

### 3. Feature Locator
Quickly find file or function containing keyword (e.g., "login", "payment").
```bash
python .agent/skills/codebase-navigator/scripts/navigator.py --action search --query "Codebase"
```
*Output: List of files and lines containing keyword.*

## Supported Languages
- Python (.py)
- JavaScript/TypeScript (.js, .ts, .jsx, .tsx)
- Java (.java)
- C# (.cs)
- Go (.go)
