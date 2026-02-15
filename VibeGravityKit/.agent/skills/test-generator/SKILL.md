---
name: test-generator
description: Generate unit/integration tests with smart edge case analysis (Zero Token Skeleton + Smart Mode).
---

# Test Generator

## Purpose
Generate test files with real test cases, not just empty stubs. Smart mode analyzes function signatures and type hints to produce null/boundary/injection edge cases automatically.

## Usage

### 1. Quick Skeleton (original)
```bash
python .agent/skills/test-generator/scripts/gen_skeleton.py src/utils.py > tests/test_utils.py
```

### 2. Smart Mode — Real Test Cases
Analyzes type hints and parameter names → generates null, boundary, XSS, large input tests:
```bash
python .agent/skills/test-generator/scripts/gen_skeleton.py src/auth.py --style smart > tests/test_auth.py
```

### 3. From Codebase Index — Full Project Coverage
Reads `codebase_index.json` from codebase-navigator → generates tests for ALL functions:
```bash
# Prerequisite: index the codebase first
python .agent/skills/codebase-navigator/scripts/navigator.py --action index --path .

# Generate tests for all indexed functions
python .agent/skills/test-generator/scripts/gen_skeleton.py --from-index --style smart > tests/test_all.py
```

### 4. Coverage Report — What's Tested vs Not
```bash
python .agent/skills/test-generator/scripts/gen_skeleton.py --from-index --coverage-report
```
Output: ✅ functions with tests, ❌ untested functions, 📈 total coverage percentage.

## Data Files
- `data/test_patterns.json` — 8 test pattern categories (unit, security, performance, E2E, database, error handling)
- `data/edge_cases.json` — 7 edge case categories with mandatory QA checklist

## Supported Languages
- Python (.py) — pytest
- JavaScript/TypeScript (.js, .ts, .jsx, .tsx) — vitest/jest
