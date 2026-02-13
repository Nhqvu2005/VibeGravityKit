---
name: code-reviewer
description: Automated code quality review with pattern-based analysis. Scans for anti-patterns, naming issues, security risks, and best practices.
---

# Code Reviewer Skill

## Purpose
Provides **zero-token code quality scanning** through regex-based pattern detection. The script scans source files and returns a structured report without consuming LLM tokens for the analysis.

## Usage

```bash
# Full scan:
python .agent/skills/code-reviewer/scripts/reviewer.py --path "src/" --action scan

# Naming convention check:
python .agent/skills/code-reviewer/scripts/reviewer.py --path "src/" --action naming

# Security-focused scan:
python .agent/skills/code-reviewer/scripts/reviewer.py --path "src/" --action security
```

## Output
Returns a JSON report with:
- `issues`: list of detected issues with file, line, severity, rule, description
- `summary`: count by severity, overall quality score (A-F)
- `suggestions`: actionable fix recommendations

## Data Files
- `review_rules.json`: All detection rules organized by category
