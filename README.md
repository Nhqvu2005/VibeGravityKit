# 🌌 VibeGravityKit

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

- **`vibegravity list`** (or `vibe list`): List all 18 specialized agents.
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

### v2.6.0
- **Smart Context Protocol** — Universal data query router across 34+ data sources (saves ~70% tokens)
- **Code Reviewer Agent** (`@[/code-reviewer]`) — Regex-based code quality scanner with 20 rules
- **Release Manager Agent** (`@[/release-manager]`) — Auto changelog, semver bumping, release notes
- **Template Marketplace** — 7 pre-built templates (SaaS, E-commerce, Blog, API, Landing, Dashboard, Mobile)

### v2.5.0
- **Leader Orchestration Mode** — Leader auto-delegates to agents, reports per phase, QA loop with smart retries (max 3)
- **Quickstart Autopilot Mode** — Fully automated end-to-end project build, QA auto-fix (max 5 retries)
- **Smart Bug Fix Rethinking** — Failed fixes trigger Meta Thinker + Planner to brainstorm alternative approaches

## ❤️ Credits
Special thanks to **[ui-ux-pro-max-skill](https://github.com/nextlevelbuilder/ui-ux-pro-max-skill)** for pioneering the data-driven approach to UI/UX generation.

## 📄 License
MIT © [Nhqvu2005](https://github.com/Nhqvu2005)
