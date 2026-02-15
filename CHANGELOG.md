# Changelog

All notable changes to **VibeGravityKit** will be documented in this file.
Format based on [Keep a Changelog](https://keepachangelog.com/).

## [2.9.0] - 2025-02-15

### Added
- **Team Profiles** — Persistent coding style, rules, and knowledge across projects
  - **Code Scanner**: Auto-detect stack, naming, comments, error handling, architecture, quotes, indent
  - **Team DNA**: 1-line compact format (~50 tokens) — injected into every agent
  - **3-Tier Memory**: Hot (always loaded) / Warm (TF-IDF search) / Cold (archived)
  - **Per-agent rule routing**: Each agent only loads its relevant rules
  - **Journal sync**: Bug fix knowledge transfers across projects — no agent hits the same bug twice
  - **Auto-learn**: Leader passively scans code + records directives at plan/phase triggers
  - **Rule Deduplication**: Jaccard similarity + stemming prevents file bloat, auto-promotes at freq ≥ 3
  - **TF-IDF dedup**: Similar journal entries auto-merge instead of duplicating
  - **Frequency decay**: Unused rules auto-demote, frequently used rules auto-promote
- **CLI**: `vibegravity team create/list/show/delete/sync/export/import`
- **CLI**: `vibegravity team scan`, `vibegravity team learn`
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

## [2.7.0] - 2025-02-14

### Added
- ⚡ **Parallel Agent Delegation** — Leader calls multiple agents simultaneously. Up to **4x faster** builds.
- 🔍 **Researcher Agent + DuckDuckGo Web Search** — Live web search using only Python stdlib (no pip, no API key). `--compact` mode for token-efficient output.
- **Meta Thinker expanded** — 45 industries, 15 frameworks, 25 archetypes, 16 monetization models, 300+ feature ideas
- **18 agents** total (was 17)

### Changed
- Leader anti-overthinking refactor
- Meta Thinker deep thinking upgrade

## [2.6.0] - 2025-02-13

### Added
- **Smart Context Protocol** — Universal data query router across 34+ data sources (saves ~70% tokens)
- **Code Reviewer Agent** (`@[/code-reviewer]`) — Regex-based code quality scanner with 20 rules
- **Release Manager Agent** (`@[/release-manager]`) — Auto changelog, semver bumping, release notes
- **Template Marketplace** — 7 pre-built templates (SaaS, E-commerce, Blog, API, Landing, Dashboard, Mobile)

## [2.5.0] - 2025-02-12

### Added
- **Leader Orchestration Mode** — Leader auto-delegates to agents, reports per phase, QA loop with smart retries (max 3)
- **Quickstart Autopilot Mode** — Fully automated end-to-end project build, QA auto-fix (max 5 retries)
- **Smart Bug Fix Rethinking** — Failed fixes trigger Meta Thinker + Planner to brainstorm alternative approaches

## [2.4.0] - 2025-02-11

### Added
- **Token Optimization** — Agent index + navigator signatures + outline for efficient context loading
- Reduced token consumption by ~40% across all agent interactions

## [2.3.0] - 2025-02-10

### Added
- **Brain Manager** — Project-level persistent context management
- **Knowledge Journal** — Development insights tracking with indexed entries
- CLI commands: `vibegravity brain`, `vibegravity journal`

## [2.2.0] - 2025-02-09

### Added
- **Environment Manager** — Auto-generate `.env.example` from codebase
- **i18n Manager** — Extract hardcoded strings for internationalization
- **Agent Memory** — Context persistence between agent sessions
- 3 new skills added

## [2.1.0] - 2025-02-08

### Added
- **Skill Enrichment** — 17 new data files added to existing skills
- Expanded data coverage for: tech-stack-advisor, seo-analyzer, market-trend-analyst, meta-thinker, and more
- Comprehensive changelog introduced

### Changed
- `vibegravity init` now installs all IDEs by default (previously required specifying IDE)

## [2.0.0] - 2025-02-07

### Added
- **Multi-IDE Support** — Cursor, Windsurf, Cline added alongside Antigravity
- `vibegravity init [ide]` to install for specific IDE
- `vibegravity update` for auto-updates
- `vibegravity doctor` for environment health checks

### Changed
- Package renamed to `VibeGravityKit`
- CLI rewritten with `click` library
- pip install fallback added to update command

## [1.0.0] - 2025-02-06

### Added
- Initial release of VibeGravityKit
- 13 specialized agents: Leader, Planner, Architect, Designer, Frontend Dev, Backend Dev, DevOps, QA, Security, SEO, Tech Writer, Meta Thinker, Knowledge Guide
- Core skill system with SKILL.md + scripts architecture
- `vibegravity init` CLI for easy setup
- MIT License
