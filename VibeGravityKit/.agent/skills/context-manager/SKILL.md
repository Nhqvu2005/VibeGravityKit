---
name: context-manager
description: Minifier & Context Controller for Token Saving.
---

# Context Manager

## Purpose
Reduces token usage by minifying code before sending it to the LLM. Strips comments and whitespace while preserving logic.

## Usage

### 1. Minify a File (Print to stdout)
```bash
python .agent/skills/context-manager/scripts/minify.py src/utils.py
```

### 2. Estimate Tokens (Simple)
(Coming soon: `token_calc.py`)

## Strategy
Use this skill in your workflows when you need to read a large file for context but don't need to edit it.
Example:
> "Read `utils.py` to understand the helper functions."
> Action: `run_command("python minify.py utils.py")`
> Result: You get the code without 500 lines of docstrings.
