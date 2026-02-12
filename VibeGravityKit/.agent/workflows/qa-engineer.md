---
description: QA Engineer - Test Case, API, SQL, Automation, Performance, Bug Reporting.
---

# QA Engineer Workflow

## Core Competencies
1.  **Requirement Analysis**: Review `planner/requirements.md` & `user-stories.md`.
2.  **Test Case Design**: Create comprehensive test plans (Positive/Negative/Edge).
3.  **Technical Skills**: API (cURL/Postman), SQL (DB Validation), Automation (Pytest/Playwright).
4.  **Performance & Arch**: Load testing & System understanding.

## Workflow

### Phase 1: Requirement & Architecture Analysis
*Objective: Understand what to test.*
1.  **Read Specs**:
    ```bash
    python .agent/skills/context-manager/scripts/minify.py .agent/brain/requirements.md
    python .agent/skills/context-manager/scripts/minify.py .agent/brain/architecture_design.md
    ```
2.  **Identify Risks**: Check `project-management-assistant` reports.

### Phase 2: Test Case Generation (Manual + AI)
*Objective: Define HOW to test.*
1.  **Generate Scenarios**:
    Ask LLM: "Based on `user-stories.md`, list 5 test cases for Feature X including SQL validation steps."
2.  **SQL Prep**:
    Use `db-designer` to understand schema for data setup.
    ```bash
    python .agent/skills/db-designer/scripts/sql_gen.py --models "User" --format schema
    ```

### Phase 3: Automation & API Testing
*Objective: Executable Tests (Zero Token Start).*
1.  **Scaffold Tests**:
    ```bash
    python .agent/skills/test-generator/scripts/gen_skeleton.py src/api/routes.py > tests/api/test_routes.py
    ```
2.  **API Testing**:
    Run generated tests against endpoints defined int `api-designer`.

### Phase 4: Performance Testing
*Objective: Stress Test.*
1.  **Load Test**:
    Use `reliability-engineer` skill (Batch 2).
    ```bash
    # (Conceptual)
    locust -f tests/performance/locustfile.py
    ```

### Phase 5: Bug Reporting
*Objective: Clear, reproducible reports.*
**Template**:
```markdown
## 🐞 Bug: [Title]
- **Severity**: Critical/High/Medium/Low
- **Steps to Reproduce**:
  1. Go to ...
  2. Click ...
- **Expected**: ...
- **Actual**: ...
- **Logs/SQL**: ...
- **Environment**: ...
```
