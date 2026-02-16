---
name: system-diagrammer
description: Generates system architecture diagrams (C4, Sequence) using Mermaid.js.
---

# System Diagrammer

## Purpose
Quickly creates architecture diagrams for PRDs or Tech Specs. Output is Mermaid.js code compatible with GitHub/Notion.

## Usage

### 1. C4 Context Diagram (High-level)
```bash
python .agent/skills/system-diagrammer/scripts/diagram.py --type c4 --title "E-commerce System" --nodes "User, Web App, API Gateway, Order Service, Database"
```

### 2. Sequence Diagram (Process Flow)
Use format `A->B:Message`.
```bash
python .agent/skills/system-diagrammer/scripts/diagram.py --type sequence --title "Login Flow" --steps "User->Web:Click Login, Web->API:POST /login, API->DB:Validate User, DB->API:User Found, API->Web:Return Token"
```

### Output
Script returns a ready-to-use `mermaid` code block.
