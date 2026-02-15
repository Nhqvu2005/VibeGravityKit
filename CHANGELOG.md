# Changelog

All notable changes to **VibeGravityKit** will be documented in this file.
Format based on [Keep a Changelog](https://keepachangelog.com/).

## [3.0.0] - 2025-02-15

### Added
- **Team Profiles** — Persistent coding style, rules, and knowledge across projects
  - **Code Scanner**: Auto-detect stack, naming, comments, error handling, architecture, quotes, indent
  - **Team DNA**: 1-line compact format (~50 tokens) — injected into every agent
  - **3-Tier Memory**: Hot (always loaded) / Warm (TF-IDF search) / Cold (archived)
  - **Per-agent rule routing**: Each agent only loads its relevant rules
  - **Journal sync**: Bug fix knowledge transfers across projects — no agent hits the same bug twice
  - **Auto-learn**: Agents detect repeated directives → auto-add to team rules
  - **TF-IDF dedup**: Similar journal entries auto-merge instead of duplicating
  - **Frequency decay**: Unused rules auto-demote, frequently used rules auto-promote
- **CLI**: `vibegravity team create/list/show/delete/sync/export/import`
- **CLI**: `vibegravity team rule add/list/remove`
- **CLI**: `vibegravity init --team <name>` flag for team injection
- **Workflow integration**: Leader and Quickstart auto-read team DNA and rules

### Changed
- Quickstart intro rewritten in English (was Vietnamese)
- README restructured: new Team Profiles section with detailed documentation
- CLI commands section converted to table format
- Agent count: 18 agents + 1 new skill (team-manager)

## [2.8.0] - 2025-02-15

### Added
- **Deployment Wizard** — New skill to deploy local websites via Cloudflare Tunnel
  - `--find-port` pre-flight scan: finds free port before starting anything
  - `--serve-cmd <stack>` lookup: returns exact serve command for 13 stacks
  - `--quiet` agent mode: machine-parseable output (FREE_PORT=, SERVE_CMD=, TUNNEL_URL=)
  - Port conflict detection with process identification
  - Auto-install cloudflared binary (Windows/macOS/Linux)
- **Deploy Templates** (`deploy_templates.json`) — Per-stack serve commands for token-efficient deployment
  - Stacks: static, react, vite, nextjs, nuxt, django, flask, fastapi, express, php, hugo, ruby, custom
- **Deploy Recipe** (`deploy_recipe.md`) — Compact 30-line agent prompt template
  - "Textbook switching" pattern: devops.md points to recipe only when deploying
- **Tech Stack Advisor** expanded to 10 categories / 56+ technologies / 25 full-stack combos
  - New categories: mobile, devops, ai_ml, auth, testing, messaging, cms
  - New flags: `--list`, `--stack`, `--json`

### Changed
- `devops.md` workflow slimmed: Step 4 reduced from 70 → 2 lines (pointer to recipe)
- `SKILL.md` for deployment-wizard slimmed from 79 → 35 lines
- Token optimization: agent only loads deploy docs when actually deploying

## [2.7.0] - Previous

### Added
- 18 specialized agents (Leader, Planner, Architect, Designer, Frontend, Backend, DevOps, QA, Security, etc.)
- 30+ skills with zero-token scripts
- Context Router for smart data retrieval
- Meta Thinker with brainstorm frameworks
- Market Trend Analyst with web search
- UI/UX Pro Max design system generator
- Brain Manager for project context
- Journal Manager for development insights
- Release Manager for version automation
- VibeCLI (`vibegravity init/update`) for easy setup
