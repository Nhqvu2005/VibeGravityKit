# 🌌 VibeGravityKit

> **The AI-Native Software House in a Box.**
> *Build enterprise-grade software with a team of 17 AI Agents — optimized for maximum speed and minimum token costs.*

---

## 🚀 How It Works — Two Ways to Build

VibeGravityKit gives you **two powerful work modes** to build software with your AI team:

### Mode 1: `@[/leader]` — Smart Delegation (Recommended)

> **You are the Boss. The Leader is your right hand.**

```
You → Leader → Agents → Report back per phase → You approve → Next phase
```

**Flow:**
1. Tell the Leader what you want to build.
2. Leader analyzes, brainstorms, and presents a plan.
3. **You approve the plan** ✅
4. Leader **auto-delegates** to the right agents:

| Phase | Agent | What Happens |
|-------|-------|-------------|
| 📋 Planning | `@[/planner]` | PRD, user stories, timeline |
| 🏗️ Architecture | `@[/architect]` | DB schema, API design, diagrams |
| 🎨 Design | `@[/designer]` | UI/UX system, components, palette |
| 💻 Development | `@[/frontend-dev]` `@[/backend-dev]` | Build the product |
| 🧪 QA & Fix | `@[/qa-engineer]` | Test → Find bugs → Fix → Retest |
| 🚀 Launch | `@[/devops]` `@[/security-engineer]` | Deploy, audit, docs |

5. **After each phase**, Leader reports results and waits for your approval.
6. **QA Smart Loop**: If a bug can't be fixed, Leader calls `@[/meta-thinker]` + `@[/planner]` to rethink the approach. Max **3 retries** — then reports to you with analysis.

**Example:**
```
You: "Build me a Spotify clone with Next.js"
Leader: [Analyzes → Plans → Reports] "Here's the plan: 6 phases, 3 weeks..."
You: "Approved ✅"
Leader: [Auto-delegates to Planner → Architect → Designer → Dev → QA → Deploy]
        [Reports after each phase for your review]
```

---

### Mode 2: `@[/quickstart]` — Full Autopilot

> **One command. Complete project. No approvals needed.**

```
You → Quickstart → [Auto-runs ALL agents] → Delivers complete project
```

**Perfect for:** MVPs, prototypes, hackathons, or when you just want results fast.

**How it works:**
1. Describe your idea.
2. Quickstart runs **every phase automatically** — no checkpoints.
3. Built-in **QA Auto-Fix Loop**: finds bugs → fixes them → retests. If stuck, calls `@[/meta-thinker]` + `@[/planner]` to rethink. Max **5 retries** per bug.
4. Delivers a **complete report** at the end: what was built, test results, unresolved issues (if any), and how to run it.

**Example:**
```
You: "@[/quickstart] Build a task management app with React + Express + PostgreSQL"
Quickstart: [Runs everything automatically...]
Quickstart: "✅ Done! Here's your report: 12 features built, 47/50 tests passing,
             3 unresolved edge cases documented. Run `npm run dev` to start."
```

---

### Mode Comparison

| | `@[/leader]` | `@[/quickstart]` |
|---|---|---|
| **User involvement** | Approve each phase | None (fully auto) |
| **Bug fix retries** | 3 max | 5 max |
| **Smart rethinking** | ✅ Meta Thinker + Planner | ✅ Meta Thinker + Planner |
| **Speed** | Careful & thorough | Fast |
| **Best for** | Production apps, critical projects | MVPs, prototypes, demos |

---

## 🎩 What is VibeGravityKit?

Imagine having a full-stack engineering team living inside your IDE.
**VibeGravityKit** turns your IDE into a coordinated squad of **15 specialized agents**, from the **Architect** who designs your database, to the **Meta Thinker** who expands your vision.

But here's the killer feature: **We hate wasting tokens.**
- **Context Manager**: Minifies your code before the AI sees it. (Saves ~50% tokens).
- **Context Router**: Queries only relevant data from 34+ data sources. (Saves ~70% tokens).
- **Diff Applier**: Applies surgical patches instead of rewriting files. (Saves ~90% tokens).

---

## ️ Installation

### Global Install (Recommended)
```bash
git clone https://github.com/Nhqvu2005/VibeGravityKit.git
cd VibeGravityKit
pip install .
```
*(Requires Python 3.9+ & Node.js 18+)*

**Usage in a new project:**
```bash
cd my-project
vibegravity init
# → Installs for ALL IDEs at once (Antigravity + Cursor + Windsurf + Cline)
```

## 🛠️ CLI Commands

- **`vibegravity list`** (or `vibe list`): List all 17 specialized agents.
- **`vibegravity doctor`**: Check your environment health (Python, Node, Git, etc.).
- **`vibegravity update`**: Auto-update VibeGravityKit to the latest version (works via Git or Pip).
- **`vibegravity version`**: Show current version.

## 🌐 Multi-IDE Support

VibeGravityKit works natively with **4 AI IDEs**:

| IDE | Command | Creates |
|-----|---------|---------|
| **Antigravity** | `vibegravity init antigravity` | `.agent/` (workflows + skills) |
| **Cursor** | `vibegravity init cursor` | `.cursor/rules/*.mdc` |
| **Windsurf** | `vibegravity init windsurf` | `.windsurf/rules/*.md` |
| **Cline** | `vibegravity init cline` | `.clinerules/*.md` |

```bash
# Example: Setup for Cursor IDE
cd my-project
vibegravity init cursor
# → 17 agent rules installed in .cursor/rules/
```

---

## 🎮 The 17 Agents (Usage Examples)

In VibeGravityKit, **You are the Boss.** Just chat with your agents using `@` mentions.

### 1. Strategy & Vision Team 🧠
**@[/leader]** (The Boss's Right Hand)
> "I want to build a Spotify clone. Orchestrate the entire plan."
*(Orchestrates all agents, reports per phase, manages QA loop)*

**@[/quickstart]** (Full Autopilot)
> "Build me a task management app with React and Express."
*(Runs everything end-to-end, delivers complete project with report)*

**@[/meta-thinker]** (Creative Advisor)
> "I want to build a food delivery app but make it unique. Brainstorm ideas."
*(Generates: `vision_brief.md` with trends, competitors, and unique angles)*

**@[/planner]** (Project Manager)
> "Break down the 'User Profile' feature into 5 user stories with acceptance criteria."
*(Generates: `user-stories.md`)*

**@[/market-trend-analyst]** (Researcher)
> "Analyze the top 3 competitors for a clear-to-do list app in 2025."
*(Generates: `market-analysis.md`)*

**@[/tech-stack-advisor]** (CTO)
> "Recommend a tech stack for a high-frequency trading bot in Python."
*(Generates: `tech-stack.md`)*

### 2. Design & Product Team 🎨
**@[/architect]** (System Architect)
> "Design a Prisma schema for a multi-tenant SaaS with subscription billing."
*(Generates: `schema.prisma`)*

**@[/designer]** (UI/UX Expert)
> "Create a dark-mode optimized color palette and Tailwind config for a crypto dashboard."
*(Generates: `tailwind.config.js`)*

**@[/mobile-wizard]** (Mobile Lead)
> "Scaffold a new Expo Router project with TypeScript and NativeWind."
*(Runs: `npx create-expo-app`)*

### 3. Engineering Team 💻
**@[/frontend-dev]** (Web Developer)
> "Implement the 'Login with Google' button using NextAuth.js."
*(Updates: `src/components/Login.tsx` using `diff-applier`)*

**@[/backend-dev]** (API Developer)
> "Create a POST /api/orders endpoint that validates input with Zod."
*(Updates: `src/app/api/route.ts`)*

**@[/devops]** (Infra Engineer)
> "Generate a Dockerfile and docker-compose.yml for this Next.js + Postgres app."
*(Generates: `Dockerfile`, `docker-compose.yml`)*

### 4. Quality & Support Team 🛡️
**@[/knowledge-guide]** (Code Explainer & Scribe)
> "Explain how the authentication flow works in this project."
*(Explains code & captures improvement ideas to `.agent/memory/ideas_inbox.md`)*

**@[/qa-engineer]** (Tester)
> "Generate unit tests for the `calculateTax` function in `utils.ts`."
*(Generates: `tests/utils.test.ts`)*

**@[/security-engineer]** (Security Officer)
> "Scan the project for hardcoded secrets and OWASP vulnerabilities."
*(Runs: `vuln_scan.py`)*

**@[/tech-writer]** (Docs Specialist)
> "Write a RELEASE_NOTES.md for version 1.0 explaining the new features."
*(Generates: `RELEASE_NOTES.md`)*

**@[/seo-specialist]** (Growth Hacker)
> "Check `index.html` for missing meta tags and open graph data."
*(Runs: `seo_check.py`)*

**@[/code-reviewer]** (Code Quality)
> "Scan the src/ folder for anti-patterns, security issues, and naming problems."
*(Runs: `reviewer.py` → Quality Score A-F)*

**@[/release-manager]** (Release Engineer)
> "Generate a changelog since v2.0.0 and bump the version to 2.6.0."
*(Runs: `release.py` → CHANGELOG.md + version bump)*

---

## 📂 Project Structure

```bash
.agent/
├── workflows/       # The "Brain": Instructions for each Role
├── skills/          # The "Hands": Python scripts that do the work
└── brain/           # Project Context & Memory
```

## 🧰 Smart Context Protocol

Instead of agents reading entire data files (hundreds of lines each), they query the **Context Router** for just what they need:

```bash
# Search across ALL 34 data sources:
python .agent/skills/context-router/scripts/context_router.py --query "fintech"
# → Returns only matching entries (saves ~70% tokens)

# Search within a specific skill:
python .agent/skills/context-router/scripts/context_router.py --skill meta-thinker --query "SCAMPER"

# List all available data:
python .agent/skills/context-router/scripts/context_router.py --list
```

## 📦 Template Marketplace

Start new projects instantly with pre-built templates:

```bash
# Browse 7 templates:
python .agent/skills/template-marketplace/scripts/template_engine.py --action list

# Get details of a template:
python .agent/skills/template-marketplace/scripts/template_engine.py --action show --template saas

# Available: saas, ecommerce, blog, api, landing, dashboard, mobile
```

## 📋 Changelog

### v2.6.0
- **Smart Context Protocol** — Universal data query router across 34+ data sources (saves ~70% tokens)
- **Code Reviewer Agent** (`@[/code-reviewer]`) — Regex-based code quality scanner with 20 rules
- **Release Manager Agent** (`@[/release-manager]`) — Auto changelog, semver bumping, release notes
- **Template Marketplace** — 7 pre-built templates (SaaS, E-commerce, Blog, API, Landing, Dashboard, Mobile)
- Agent count updated to **17**

### v2.5.0
- **Leader Orchestration Mode** — Leader auto-delegates to agents, reports per phase, QA loop with smart retries (max 3)
- **Quickstart Autopilot Mode** — Fully automated end-to-end project build, QA auto-fix (max 5 retries)
- **Smart Bug Fix Rethinking** — Failed fixes trigger Meta Thinker + Planner to brainstorm alternative approaches

### v2.4.0
- `agent_index.json` — Leader reads 1 file to know all agents, their roles, skills, and when to call each
- `codebase-navigator` upgraded — now captures full function signatures (params, return types)
- New action: `--action outline` for compact codebase overview
- Handoff template for standardized task delegation between agents
```bash
# Leader reads this to decide who to call:
cat .agent/brain/agent_index.json

# Index codebase with full signatures:
python .agent/skills/codebase-navigator/scripts/navigator.py --action index --path "."

# Compact outline for Leader (1 line per file):
python .agent/skills/codebase-navigator/scripts/navigator.py --action outline
# Output: src/api.py → create_user:15, get_orders:42, authenticate:78

# Full map with signatures:
python .agent/skills/codebase-navigator/scripts/navigator.py --action map
# Output: L15: def create_user(name, email, role="user")

# Search by function name or signature:
python .agent/skills/codebase-navigator/scripts/navigator.py --action search --query "auth"
```

### v2.3.0
- New skill: `brain-manager` — project context, architecture decisions, export/import
- New skill: `journal-manager` — 2-tier knowledge journal (index + entries)
```bash
vibegravity brain show                              # View project context
vibegravity brain add-decision "Use PostgreSQL"     # Record decision
vibegravity brain set project.name "MyApp"          # Set value
vibegravity brain export -o backup.json             # Backup brain
vibegravity journal add -t "Fix N+1 query" --tags "perf,db"  # Record lesson
vibegravity journal list                            # View recent entries
vibegravity journal search "database"               # Search
```

### v2.2.0
- New skill: `env-manager` — auto-scan codebase and generate `.env.example`
- New skill: `i18n-manager` — extract hardcoded strings for translation
- Agent Memory: `project_context.json` for project knowledge
```bash
python .agent/skills/env-manager/scripts/env_scanner.py --path "."
python .agent/skills/i18n-manager/scripts/string_extractor.py --path "src/"
```

### v2.1.0
- 17 new data files: API patterns, DB schemas, Docker/CI-CD templates, security scanning (OWASP), SEO rules, mobile templates, and more

### v2.0.0
- CLI: `vibegravity init`, `list`, `doctor`, `update`, `version`
- Multi-IDE: Cursor (`.mdc`), Windsurf (`.md`), Cline (`.md`)
```bash
vibegravity init                   # Install for ALL IDEs at once
vibegravity init cursor            # Install for Cursor only
vibegravity list                   # List all 17 agents
vibegravity doctor                 # Check environment health
vibegravity update                 # Auto-update to latest version
```

## ❤️ Credits
Special thanks to **[ui-ux-pro-max-skill](https://github.com/nextlevelbuilder/ui-ux-pro-max-skill)** for pioneering the data-driven approach to UI/UX generation.

## 📄 License
MIT © [Nhqvu2005](https://github.com/Nhqvu2005)
