---
name: architecture-auditor
description: Reviews architecture, checks standards, security, and technical debt.
---

# Architecture Auditor

## Purpose
Ensures system quality by auditing standards for Security, Performance, Naming Conventions, and Technical Debt. Replaces 4 individual skills.

## Usage

### 1. Security Audit
Checks common security vulnerabilities (OWASP Top 10 checklist).
```bash
python .agent/skills/architecture-auditor/scripts/auditor.py --check security
```

### 2. Performance Audit
Checklist for performance optimization (Frontend & Backend).
```bash
python .agent/skills/architecture-auditor/scripts/auditor.py --check performance
```

### 3. Naming Convention Check
Standard naming for Project (Variables, Classes, DB Tables).
```bash
python .agent/skills/architecture-auditor/scripts/auditor.py --check naming
```

### 4. Technical Debt Guardian
Identifies signs of technical debt (Code smells, Anti-patterns).
```bash
python .agent/skills/architecture-auditor/scripts/auditor.py --check debt
```
