---
name: security-scanner
description: Scan code for vulnerabilities (Regex SAST) & Generate Security Checklist.
---

# Security Scanner

## Purpose
Quickly check codebase for hardcoded secrets and dangerous functions, and generate a standardized Security Release Checklist.

## Usage

### 1. Zero-Token Audit (SAST)
```bash
python .agent/skills/security-scanner/scripts/vuln_scan.py .
```

### 2. Generate Release Checklist
```bash
python .agent/skills/security-scanner/scripts/checklist_gen.py > SECURITY_GATE.md
```
