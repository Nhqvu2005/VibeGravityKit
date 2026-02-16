---
description: QA Engineer - Index-First Testing, Edge Cases, Security, Performance, Bug Reporting.
---

# QA Engineer Workflow

> ⚠️ **MANDATORY**: Read this ENTIRE file before starting work.
> Follow the steps IN ORDER. Read the SKILL.md for each skill before using it.
> Also read `.agent/brain/phase_context.md` for project context.

## Core Principle
**Index First → Coverage Analysis → Smart Test Generation → Edge Case Validation**

Never write tests blindly. Always understand the full codebase structure first, then generate tests systematically to ensure complete coverage.

## Phase 1: Codebase Discovery

*Objective: Understand ALL code that needs testing.*

1. **Index the codebase** (if not already indexed):
   ```bash
   python .agent/skills/codebase-navigator/scripts/navigator.py --action index --path .
   ```
2. **View project map** — understand structure:
   ```bash
   python .agent/skills/codebase-navigator/scripts/navigator.py --action outline
   ```
3. **Read specs** (if available):
   ```bash
   python .agent/skills/context-manager/scripts/minify.py .agent/brain/requirements.md
   ```

## Phase 2: Coverage Analysis

*Objective: Know what is tested and what is NOT.*

1. **Run coverage report**:
   ```bash
   python .agent/skills/test-generator/scripts/gen_skeleton.py --from-index --coverage-report
   ```
   Output shows: ✅ tested functions, ❌ untested functions, 📈 coverage %

2. **Prioritize by severity** — refer to `test_patterns.json > test_severity_matrix`:
   - 🔴 **Critical** (always test): Auth, payments, data mutations, user registration
   - 🟡 **High** (should test): CRUD, search, pagination, file upload
   - 🟢 **Medium** (nice to test): Sorting, caching, admin features

## Phase 3: Test Generation

*Objective: Generate tests for ALL untested functions.*

1. **Smart skeleton** (reads type hints, generates edge cases):
   ```bash
   python .agent/skills/test-generator/scripts/gen_skeleton.py --from-index --style smart > tests/test_generated.py
   ```
2. **Single file** (when working on specific feature):
   ```bash
   python .agent/skills/test-generator/scripts/gen_skeleton.py src/auth/login.py --style smart > tests/test_login.py
   ```
   Smart mode auto-generates:
   - Valid input case
   - Null/None for each parameter
   - Empty string/collection for each parameter
   - Zero and negative for numeric parameters
   - Boundary values (MAX_INT, very long strings)
   - XSS/injection payloads for text inputs
   - Large input stress tests

3. **Review and customize** — generated tests are starting points. The agent MUST:
   - Update import paths
   - Add expected return values
   - Add business logic assertions (not just `is not None`)

## Phase 4: Edge Case Checklist (MANDATORY)

*Objective: Verify hard edge cases that catch real bugs.*

Before reporting tests as "done", verify EVERY item in this checklist.
Reference: `.agent/skills/test-generator/data/edge_cases.json`

### Input Validation
- [ ] Null/None for every required parameter
- [ ] Empty string for every text parameter
- [ ] Zero for every numeric parameter
- [ ] Negative number for every numeric parameter
- [ ] Empty array/dict for every collection parameter
- [ ] Very long string (10K+ chars) for at least 1 text input
- [ ] Unicode/emoji input
- [ ] SQL injection payload: `' OR '1'='1`
- [ ] XSS payload: `<script>alert(1)</script>`

### Auth & Security
- [ ] Unauthenticated request → 401
- [ ] Expired token → 401
- [ ] Wrong permissions → 403
- [ ] IDOR (access another user's resource) → 403
- [ ] Path traversal: `../../etc/passwd` → 400

### Error Handling
- [ ] Network timeout → graceful error
- [ ] Server 500 → meaningful error message
- [ ] Malformed JSON response → handled
- [ ] Database connection failure → handled

### State & Concurrency
- [ ] Double-submit form → only 1 record created
- [ ] Fresh install (no data) → doesn't crash
- [ ] Large dataset (10K+ records) → still performs

## Phase 5: API Testing

*Objective: Test all API endpoints systematically.*

For each endpoint, test:
```
┌─────────────┬──────────────────────────────────┐
│ Test Type   │ What to verify                   │
├─────────────┼──────────────────────────────────┤
│ Happy path  │ Valid input → correct response    │
│ Validation  │ Invalid input → 400 + error msg  │
│ Auth        │ No token → 401, wrong role → 403 │
│ Not found   │ Invalid ID → 404                 │
│ Duplicate   │ Create same resource → 409       │
│ Pagination  │ ?page=1&limit=10 → correct count │
│ Search      │ ?q=keyword → filtered results    │
│ Sorting     │ ?sort=name → correct order       │
└─────────────┴──────────────────────────────────┘
```

## Phase 6: Browser/E2E Testing

*Objective: Test critical user flows in real browser.*

Use the browser tool to verify:
1. **Login flow** — email → password → submit → redirect to dashboard
2. **Form validation** — submit empty → errors shown, fill required → errors clear
3. **Navigation** — all links work, back/forward behaves correctly
4. **Responsive** — mobile viewport (375px) → layout adapts
5. **Error states** — API down → error message shown, retry button works

Reference templates: `test_patterns.json > e2e_browser_test`

## Phase 7: Performance Testing (When Applicable)

*Objective: Ensure app handles load.*

1. **Response time** — API endpoints respond within 200ms
2. **Concurrent requests** — 100 simultaneous requests → no failures
3. **Large data** — 10K+ records → pagination works, no timeout
4. **Memory** — processing large input doesn't leak memory

Reference: `test_patterns.json > performance_test > locust_template`

## Phase 8: Bug Reporting

*Objective: Clear, reproducible bug reports.*

```markdown
## 🐞 Bug: [Title]
- **Severity**: Critical / High / Medium / Low
- **Component**: [File/Module where bug occurs]
- **Steps to Reproduce**:
  1. Go to ...
  2. Input: [exact value that triggers bug]
  3. Click ...
- **Expected**: ...
- **Actual**: ...
- **Root Cause** (if known): ...
- **Suggested Fix** (if known): ...
- **Logs/SQL**: [relevant error output]
- **Environment**: [OS, browser, Node/Python version]
```

## Quick Reference

| What | Command |
|------|---------|
| Index codebase | `navigator.py --action index --path .` |
| View outline | `navigator.py --action outline` |
| Coverage report | `gen_skeleton.py --from-index --coverage-report` |
| Generate smart tests | `gen_skeleton.py --from-index --style smart` |
| Single file test | `gen_skeleton.py src/file.py --style smart` |
| Run Python tests | `pytest tests/ -v --tb=short` |
| Run JS tests | `npx vitest run` |
| Run coverage | `pytest --cov=src tests/` or `npx vitest --coverage` |
