---
name: tech-stack-advisor
description: Suggests suitable tech stack based on project requirements using local database.
---

# Tech Stack Advisor

## Purpose
Recommends the best Technology Stack across **10 categories** (56+ technologies) and **25 full-stack combos**.
Also supports scanning legacy codebases and comparing tech options.

## Categories
| Category | Count | Examples |
|----------|-------|---------|
| frontend | 7 | React, Vue, Angular, Svelte, Next.js, Astro, HTMX |
| backend | 8 | Node.js, Python, Go, Rust, Java, C#, PHP, Elixir |
| database | 7 | PostgreSQL, MySQL, MongoDB, Redis, SQLite, Supabase, Firebase |
| mobile | 5 | React Native, Flutter, SwiftUI, Kotlin, Ionic |
| devops | 6 | Docker, Kubernetes, GitHub Actions, Terraform, Vercel, Railway |
| ai_ml | 5 | OpenAI, LangChain, Hugging Face, Ollama, Vector DBs |
| auth | 5 | Clerk, Auth0, Supabase Auth, NextAuth, Keycloak |
| testing | 5 | Vitest, Playwright, Cypress, Jest, pytest |
| messaging | 4 | RabbitMQ, Kafka, BullMQ, Celery |
| cms | 4 | WordPress, Strapi, Sanity, Payload |

## Usage

### 1. List All Categories
```bash
python .agent/skills/tech-stack-advisor/scripts/advisor.py --list
```

### 2. Recommend by Category + Keywords
```bash
python .agent/skills/tech-stack-advisor/scripts/advisor.py --category web --keywords "seo,fast"
python .agent/skills/tech-stack-advisor/scripts/advisor.py --category ai_ml --keywords "rag,enterprise"
python .agent/skills/tech-stack-advisor/scripts/advisor.py --category fullstack --keywords "typescript,realtime"
```

### 3. Recommend Full-Stack Combos
```bash
python .agent/skills/tech-stack-advisor/scripts/advisor.py --stack --keywords "saas,react,seo"
```

### 4. Compare Technologies
```bash
python .agent/skills/tech-stack-advisor/scripts/advisor.py --compare --category frontend
python .agent/skills/tech-stack-advisor/scripts/advisor.py --compare --category database
```

### 5. Legacy Project Scan
```bash
python .agent/skills/tech-stack-advisor/scripts/scanner.py --path "."
```

## Category Aliases
- `web` → frontend + backend + database
- `fullstack` → frontend + backend + database + devops
- `all` → all 10 categories
