# 🌌 VibeGravityKit

> **The AI-Native Software House in a Box.**
> *Build enterprise-grade software with a team of 13 AI Agents — optimized for maximum speed and minimum token costs.*

---

## 🎩 What is VibeGravityKit?

Imagine having a full-stack engineering team living inside your IDE. 
**VibeGravityKit** turns your IDE into a coordinated squad of **13 specialized agents**, from the **Architect** who designs your database, to the **Meta Thinker** who expands your vision.

But here's the killer feature: **We hate wasting tokens.**
- **Context Manager**: Minifies your code before the AI sees it. (Saves ~50% tokens).
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

- **`vibegravity list`** (or `vibe list`): List all 13 specialized agents.
- **`vibegravity doctor`**: Check your environment health (Python, Node, Git, etc.).
- **`vibegravity update`**: Auto-update VibeGravityKit to the latest version (works via Git or Pip).
- **`vibegravity version`**: Show current version (v2.0.0).

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
# → 14 agent rules installed in .cursor/rules/
```

---

## 🎮 The 13 Agents (Usage Examples)

In VibeGravityKit, **You are the Boss.** Just chat with your agents using `@` mentions.

### 1. Strategy & Vision Team 🧠
**@[/leader]** (The Boss's Right Hand)
> "I want to build a Spotify clone. Orchestrate the entire plan."
*(Orchestrates Planner, Architect, and Devs automatically)*

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

---

## 📂 Project Structure

```bash
.agent/
├── workflows/       # The "Brain": Instructions for each Role
├── skills/          # The "Hands": Python scripts that do the work
└── brain/           # Project Context & Memory
```

## 📋 Changelog

### v2.3.0
- New skill: `brain-manager` — project context, architecture decisions, export/import brain
- New skill: `journal-manager` — 2-tier knowledge journal (index + entries)
- CLI commands: `vibegravity brain show`, `vibegravity brain add-decision`, `vibegravity journal add`, `vibegravity journal search`
- Auto-save triggers for journal (≥3 attempts, ≥5 files, rollback)

### v2.2.0
- New skill: `env-manager` — auto-scan codebase and generate `.env.example`
- New skill: `i18n-manager` — extract hardcoded strings for translation
- Agent Memory: `project_context.json` template for storing project knowledge and decisions

### v2.1.0
- 17 new data files: API patterns, DB schemas, Docker/CI-CD templates, security scanning (OWASP), SEO rules, mobile templates, task estimation, and more
- Changelog section added to README

### v2.0.0
- CLI commands: `vibegravity init`, `list`, `doctor`, `update`, `version`
- Multi-IDE support: Cursor (`.mdc`), Windsurf (`.md`), Cline (`.md`)
- `vibegravity init` installs for all 4 IDEs at once
- `generate_adapters.py` auto-converts workflows to IDE rule files

## ❤️ Credits
Special thanks to **[ui-ux-pro-max-skill](https://github.com/nextlevelbuilder/ui-ux-pro-max-skill)** for pioneering the data-driven approach to UI/UX generation.

## 📄 License
MIT © [Nhqvu2005](https://github.com/Nhqvu2005)
