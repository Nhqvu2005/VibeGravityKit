# Changelog

All notable changes to **VibeGravityKit** will be documented in this file.
Format based on [Keep a Changelog](https://keepachangelog.com/).

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
