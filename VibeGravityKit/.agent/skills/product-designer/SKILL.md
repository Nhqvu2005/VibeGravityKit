---
name: product-designer
description: Understand users, draw flows, check usability, and handoff to dev.
---

# Product Designer (UX & Process)

## Purpose
Supplements Designer with "Soft" and "Process" skills: User Research, Flow Logic, Usability Testing, and Standard Dev Handoff.

## Usage

### 1. User Research
Create Persona to understand user pain points/needs.
```bash
python .agent/skills/product-designer/scripts/ux_tools.py --action persona --type "mobile_shopper"
```

### 2. Flow Logic (Wireflow)
Draft main steps in User Flow before UI design.
```bash
python .agent/skills/product-designer/scripts/ux_tools.py --action flow --task "checkout"
```

### 3. Usability Check (Heuristics)
Checklist of 10 Nielsen Usability Heuristics.
```bash
python .agent/skills/product-designer/scripts/ux_tools.py --action usability
```

### 4. Dev Handoff & Tech Limits
Checklist for design handoff, ensuring feasibility (Mobile/Web constraints).
```bash
python .agent/skills/product-designer/scripts/ux_tools.py --action handoff --platform "mobile_app"
```
*Platform: `web` or `mobile_app`*
