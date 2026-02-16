# 🌌 VibeGravityKit

[![Release](https://img.shields.io/badge/Release-v2.9.0-blue?style=flat-square)](https://github.com/Nhqvu2005/VibeGravityKit/releases)
[![Agents](https://img.shields.io/badge/AI_Agents-18-blueviolet?style=flat-square)](https://github.com/Nhqvu2005/VibeGravityKit)
[![Reasoning Rules](https://img.shields.io/badge/Reasoning_Rules-101-brightgreen?style=flat-square)](https://github.com/Nhqvu2005/VibeGravityKit)
[![UI Styles](https://img.shields.io/badge/UI_Styles-68-orange?style=flat-square)](https://github.com/Nhqvu2005/VibeGravityKit)
[![Python](https://img.shields.io/badge/Python-3.x-3776AB?style=flat-square&logo=python&logoColor=white)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)](https://github.com/Nhqvu2005/VibeGravityKit/blob/main/LICENSE)

[![CLI](https://img.shields.io/badge/CLI-v2.9.0-blue?style=flat-square&logo=gnubash&logoColor=white)](https://github.com/Nhqvu2005/VibeGravityKit)
[![Skills](https://img.shields.io/badge/Skills-42-blue?style=flat-square)](https://github.com/Nhqvu2005/VibeGravityKit)
[![Workflows](https://img.shields.io/badge/Workflows-18-blue?style=flat-square)](https://github.com/Nhqvu2005/VibeGravityKit)
[![Stars](https://img.shields.io/github/stars/Nhqvu2005/VibeGravityKit?style=flat-square&logo=github)](https://github.com/Nhqvu2005/VibeGravityKit/stargazers)
[![PayPal](https://img.shields.io/badge/PayPal-Support_Development-0070ba?style=flat-square&logo=paypal&logoColor=white)](https://paypal.me/Nhqvu2005)

<p align="center">
  <img src="https://raw.githubusercontent.com/Nhqvu2005/VibeGravityKit/main/Web.png" alt="VibeGravityKit Documentation Site" width="100%">
</p>

> **The AI-Native Software House in a Box.**
> *Build enterprise-grade software with a team of 18 AI Agents — with **parallel delegation** for maximum speed and minimum token costs.*

---


## 🎩 What is VibeGravityKit?

Imagine having a full-stack engineering team living inside your IDE.
**VibeGravityKit** turns your IDE into a coordinated squad of **18 specialized agents**, from the **Architect** who designs your database, to the **Researcher** who searches the web with DuckDuckGo.

But here's the killer feature: **We hate wasting tokens.**
- **Context Manager**: Minifies your code before the AI sees it. (Saves ~50% tokens).
- **Context Router**: Queries only relevant data from 34+ data sources. (Saves ~70% tokens).
- **Diff Applier**: Applies surgical patches instead of rewriting files. (Saves ~90% tokens).

---

## 🚀 How It Works — Two Ways to Build

VibeGravityKit gives you **two powerful work modes** to build software with your AI team:

### Mode 1: `@[/quickstart]` — Instant Noodle 🍜

> **Describe your idea → Get a working product.** Fast, automatic, delicious.
> Like instant noodles — just add water (your idea) and it's ready to eat.

```
You → Leader confirms plan → Auto-build → ♻️ Verify Loop → Deploy → Done!
```

**Perfect for:** MVPs, prototypes, demos, hackathons, or non-tech users who just want results.

**How it works:**
1. Describe your idea — even vague is fine ("I want an online store").
2. Leader auto-detects tech stack + checks template marketplace (saves ~70% tokens if match).
3. **Leader shows you a simple checklist** — you approve/edit before building.
4. Build runs **fully automatic** with parallel agents.
5. **♻️ Completion Loop (max 5)**: Leader scans codebase to verify EVERY feature in your checklist actually works. Missing or broken? → dispatches sub-agent to fix → loops until all ✅.
6. **Auto-deploys** via Cloudflare Tunnel → you get a live link immediately.

**Example:**
```
You: "Build me a simple URL shortener"
Quickstart:
  📋 Plan: [Home page ✓] [Shorten URL ✓] [Redirect ✓] [Copy link ✓]
  "Want to add or remove anything?"
You: "Looks good ✅"
Quickstart:
  🔥 Designing... → 💻 Building... → ♻️ Verifying features (2/5)...
  🚀 Done! https://xxx.trycloudflare.com
```

---

### Mode 2: `@[/leader]` — Slow & Steady 🍲

> **You are the Chef. The Leader is your sous-chef.** Full control at every step.
> Like a slow-cooked stew — takes time, but the result is production-grade quality.

```
You → Leader → Agents → Report back per phase → You approve → Next phase
```

**Perfect for:** Production apps, enterprise projects, or when quality matters more than speed.

**How it works:**
1. Tell the Leader what you want to build.
2. Leader analyzes, brainstorms, and presents a plan.
3. **You approve the plan** ✅
4. Leader **auto-delegates** to the right agents:

| Phase | Agent | What Happens | Mode |
|-------|-------|-------------|------|
| 📋 Planning | `@[/planner]` | PRD, user stories, timeline | Sequential |
| 🏗️ Architecture + 🎨 Design | `@[/architect]` + `@[/designer]` | DB schema + UI/UX system | ⚡ **PARALLEL** |
| 💻 Development | `@[/frontend-dev]` + `@[/backend-dev]` | Build frontend + backend simultaneously | ⚡ **PARALLEL** |
| 🧪 QA & Fix | `@[/qa-engineer]` | Test → Find bugs → Fix → Retest | Sequential |
| 🚀 Launch | `@[/devops]` + `@[/security]` + `@[/seo]` + `@[/docs]` | Deploy, audit, SEO, docs — all at once | ⚡ **PARALLEL** |

5. **After each phase**, Leader reports results and waits for your approval.
6. **⚡ Parallel Delegation**: Architecture + Design run at the same time. Frontend + Backend run at the same time. **Up to 4x faster.**
7. **QA Smart Loop**: If a bug can't be fixed, Leader calls `@[/meta-thinker]` + `@[/planner]` to rethink the approach. Max **3 retries**.

**Example:**
```
You: "Build me a Spotify clone with Next.js"
Leader: [Analyzes → Plans → Reports] "Here's the plan: 6 phases, 3 weeks..."
You: "Approved ✅"
Leader: [Auto-delegates to Planner → Architect → Designer → Dev → QA → Deploy]
        [Reports after each phase for your review]
```

---

### Mode Comparison

| | 🍜 `@[/quickstart]` | 🍲 `@[/leader]` |
|---|---|---|
| **Philosophy** | Instant noodle — fast & easy | Slow-cooked — careful & thorough |
| **User involvement** | Approve plan once | Approve each phase |
| **Parallel agents** | ⚡ Yes | ⚡ Yes |
| **Completion verification** | ♻️ Auto-loop (max 5) | Manual per phase |
| **Auto-deploy** | ✅ Cloudflare Tunnel | Manual |
| **Template-first** | ✅ Auto-detect | Manual |
| **Best for** | MVPs, demos, non-tech users | Production apps, critical projects |
---

## 🧬 Team Profiles — Carry Your Style Across Projects (v2.9.0)

> **Problem:** Every `vibegravity init` starts fresh — agents forget your coding style, tech preferences, and hard-won bug fixes.
> **Solution:** Persistent team profiles that **learn from you automatically** as you work, and carry that knowledge to every new project.

### Quick Start

```bash
# Step 1: Create an empty team
vibegravity team create my-team

# Step 2: Init your project with that team
vibegravity init antigravity --team my-team

# Step 3: Just work normally with @[/leader] or @[/quickstart]
# → The agents AUTO-LEARN your coding style every time you:
#    ✅ Confirm a plan  → code scanned, DNA updated
#    ✅ Complete a phase → directives you said become rules
#    ✅ Fix a bug        → journal entry synced to team
```

**That's it.** No config files, no manual setup. The team learns passively.

### How Auto-Learn Actually Works

The **leader/quickstart** agent acts as the observer. At each trigger point, it calls `team_learner.py`:

| Trigger | What Happens | Command Agent Runs |
|---------|-------------|-------------------|
| 🔵 **Plan confirmed** | Scans project source code → detects stack, naming style, architecture → generates/updates Team DNA | `team_learner.py --scan-project .` |
| 🟢 **Phase completed** | Leader observed your directives (e.g. "write in English") → passes each one as a rule | `team_learner.py --directive "write in English"` |
| 🔴 **Bug fixed** | Journal entry auto-syncs to team profile | `team_manager.py save-back` |
| 🟡 **Manual scan** | You force-scan an existing codebase (optional) | `vibegravity team scan my-team --path ./project` |
| 🟣 **Manual learn** | You ask team to learn from current project | `vibegravity team learn` |

### Data Storage

All team data is stored **globally** (survives across projects):

```
~/.vibegravity/teams/<name>/
├── team.json               ← Main metadata (name, created_at, stack, code_style)
├── hot/                     ← ALWAYS loaded (~50 tokens)
│   ├── team.dna             ← 1-line DNA string (auto-generated)
│   └── top_rules.md         ← Auto-promoted rules (frequency ≥ 3)
├── warm/                    ← Loaded on demand (TF-IDF search)
│   ├── rules.json           ← ALL rules with dedup tracking
│   └── journal/
│       ├── index.json       ← Bug fix entries (title, tags, frequency)
│       └── entries/*.md     ← Full journal entries
└── cold/                    ← Archived (0 tokens unless requested)
    └── history/             ← Old DNA versions for rollback
```

When injected into a project (`init --team`), DNA and rules are copied to `.agent/brain/`:
```
.agent/brain/
├── team_dna.txt             ← DNA string for agents to read
├── team_rules.md            ← Hot rules (always applied)
├── team_rules/              ← Per-agent rules
│   ├── global.md
│   └── frontend-dev.md
└── team_meta.json           ← Which team, injected when
```

### Rule Deduplication (Prevents File Bloat)

When a directive is added (manually or by the leader), the system checks if a **similar rule already exists** before creating a new one:

1. **Normalize** — strips filler words ("please", "always", "must", "should"...)
2. **Stem** — reduces suffixes: "documentation" → "document", "writing" → "writ"
3. **Abbreviation expand** — "docs" → "document", "ts" → "typescript"
4. **Jaccard similarity** — compares token overlap (threshold ≥ 50%)
5. **If match found** → increments `frequency` instead of creating duplicate
6. **If frequency ≥ 3** → auto-promoted to Hot tier (loaded every session)

```
Example:
  Existing rule: "write docs in English"           (freq: 2)
  New directive:  "always write documentation in English"
  → Normalized:   "write document english" = "write document english"
  → Similarity:   1.0 (exact match after normalization)
  → Result:       frequency → 3, auto-promoted to Hot 🔥
```

### rules.json Format

```json
{
  "global": ["write docs in English"],
  "rules": [
    {
      "id": 1,
      "text": "write docs in English",
      "agent": "global",
      "frequency": 3,
      "created_at": "2026-02-15T10:00:00",
      "last_used": "2026-02-15T10:28:00"
    }
  ]
}
```

### 3-Tier Memory System

| Tier | What's Stored | Token Cost | When Loaded |
|------|--------------|------------|-------------|
| 🔴 **Hot** | Team DNA (1 line) + top rules | ~50 tokens | Always — every session |
| 🟡 **Warm** | Full rules + journal index | ~200 tokens | On demand — TF-IDF search |
| 🔵 **Cold** | Archived entries + DNA history | 0 tokens | Only when you ask |

### Team DNA — Your Style in One Line

```
naming:camelCase|comments:minimal|lang:typescript+python|fe:react|be:fastapi|css:tailwind|arch:feature|indent:2
```

This compact format (~50 tokens) tells every agent exactly how you like your code. It grows automatically as you work — you never need to write it manually.

### What Gets Detected (by Code Scanner)

| Category | Detected From |
|----------|--------------|
| Tech stack | `package.json`, `requirements.txt`, `tsconfig.json` |
| Naming convention | Regex analysis: camelCase vs snake_case |
| Comment density | Lines of comments / total lines ratio |
| Error handling | try/catch frequency per function |
| Architecture | Folder structure: feature-based vs layer-based |
| Quotes, semicolons, indent | Source file analysis |

### CLI Commands

```bash
# Team management
vibegravity team create <name>                # Create empty team (learns as you work)
vibegravity team list                         # List all teams
vibegravity team show <name>                  # Show DNA + stats
vibegravity team delete <name>                # Delete team

# Learning
vibegravity team scan <name> --path <project> # Manually scan code into team (optional)
vibegravity team learn                        # Scan current project code style
vibegravity team learn --directive "text"     # Add a specific directive as rule

# Rules — explicitly teach your team
vibegravity team rule add "Always write docs in English"
vibegravity team rule add "Use Tailwind" --agent frontend-dev
vibegravity team rule list
vibegravity team rule remove <id>

# Knowledge sharing
vibegravity team sync <other-team>            # Merge another team's knowledge
vibegravity team export <name>                # Share as .zip
vibegravity team import team-file.zip         # Import from .zip
```

### The Learning Lifecycle

```
┌──────────────┐     ┌──────────────────┐     ┌────────────────┐
│  team create │────▶│  init --team     │────▶│  Work with     │
│  (empty)     │     │  (inject DNA)    │     │  leader/QS     │
└──────────────┘     └──────────────────┘     └───────┬────────┘
                                                      │
                              ┌────────────────────────┘
                              ▼
                     ┌──────────────────┐
                     │  AUTO-LEARN      │◀── plan confirmed → scan code
                     │  • Scan code     │◀── phase done → save directives
                     │  • Detect style  │◀── bug fixed → sync journal
                     │  • Update DNA    │
                     │  • Save rules    │
                     │  • Dedup check   │
                     └───────┬──────────┘
                             │
                             ▼
                     ┌──────────────────┐     ┌───────────────┐
                     │  Team DNA grows  │────▶│  Next project │
                     │  with every      │     │  inherits ALL │
                     │  project         │     │  the knowledge│
                     └──────────────────┘     └───────────────┘
```

### Auto-Learn Examples

```
Session 1: You tell leader "write all comments in English" → added to rules (freq: 1)
Session 2: You say "write comments in English" again → dedup match → freq: 2
Session 3: Third time → freq: 3 → auto-promoted to Hot rules (always applied)

Project A: Fixed "CORS issue with Vite proxy" → journal entry saved
Project B: Agent encounters CORS → searches journal → finds fix → applies instantly
```

No manual setup. No configuration files. Just work and the team gets smarter.

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
vibegravity init                              # Fresh install for ALL IDEs
vibegravity init antigravity --team my-team   # Install + inject team profile
```

## 🛠️ CLI Commands

| Command | Description |
|---------|-------------|
| `vibegravity init [ide] [--team name]` | Install for all/specific IDE, optionally with team profile |
| `vibegravity list` | List all 18 specialized agents |
| `vibegravity doctor` | Check environment health (Python, Node, Git) |
| `vibegravity update` | Auto-update to latest version |
| `vibegravity version` | Show current version |
| `vibegravity team create <name>` | Create empty team (auto-learns as you work) |
| `vibegravity team scan <name> --path <dir>` | Manually scan project code into team (optional) |
| `vibegravity team learn` | Scan conversation logs → extract habits (also runs passively) |
| `vibegravity team list / show / delete` | Manage team profiles |
| `vibegravity team rule add/list/remove` | Manage team rules |
| `vibegravity team sync <other-team>` | Merge another team's knowledge |
| `vibegravity team export / import` | Share teams as .zip |
| `vibegravity brain` | Manage project brain |
| `vibegravity journal` | Knowledge journal |

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
# → 18 agent rules installed in .cursor/rules/
```

---

## 🎮 The 18 Agents (Usage Examples)

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

**@[/researcher]** (Web Researcher)
> "Search for AI SaaS trends 2025 and top competitors."
*(Uses **DuckDuckGo API** — zero dependencies, stdlib only. `--compact` mode for token-efficient output)*

```bash
# Token-efficient search (for AI agents):
python .agent/skills/market-trend-analyst/scripts/web_search.py -q "AI trends 2025" --compact --max 5
# Output: 1 line per result → title | url
```

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

### v2.9.0
- 🧬 **Team Profiles** — Persistent coding style, rules, and knowledge across projects
  - `team create`, `team scan`, `team learn`, `team inject`, `team sync`, `team export/import`
  - **Code Scanner** — auto-detects stack, naming, architecture from source files
  - **Team DNA** — compact 1-line profile (~50 tokens) for token efficiency
  - **3-Tier Memory** (Hot/Warm/Cold) with TF-IDF search
  - **Auto-Learn** — leader passively scans code + records directives at plan/phase triggers
  - **Rule Deduplication** — Jaccard similarity + stemming prevents file bloat, auto-promotes at freq ≥ 3
  - `init --team <name>` to inject team profile on project setup

### v2.8.0
- 🚀 **Deployment Wizard** — Deploy local websites to the internet via Cloudflare Tunnel. Zero hosting, zero domain, zero config.
  - `--find-port` pre-flight scan, `--serve-cmd` per-stack lookup (13 stacks)
  - `--quiet` agent mode with machine-parseable output
- 🎯 **Token-Optimized Deploy** — "Textbook switching" pattern: devops.md points to compact recipe only when deploying
  - `deploy_recipe.md` (30 lines) replaces 70-line inline instructions
  - `deploy_templates.json` with per-stack serve commands
- 📦 **Tech Stack Advisor** expanded — 10 categories, 56+ technologies, 25 full-stack combos

### v2.7.0
- ⚡ **Parallel Agent Delegation** — Leader calls multiple agents simultaneously. Up to **4x faster** builds.
- 🔍 **Researcher Agent + DuckDuckGo Web Search** — Live web search using only Python stdlib (no pip, no API key). `--compact` mode for token-efficient output.
- **Meta Thinker expanded** — 45 industries, 15 frameworks, 25 archetypes, 16 monetization models, 300+ feature ideas
- **18 agents** total (was 17)

> 📄 **[View full changelog →](CHANGELOG.md)**

## ❤️ Credits
Special thanks to **[ui-ux-pro-max-skill](https://github.com/nextlevelbuilder/ui-ux-pro-max-skill)** for pioneering the data-driven approach to UI/UX generation.

## 📄 License
MIT © [Nhqvu2005](https://github.com/Nhqvu2005)
