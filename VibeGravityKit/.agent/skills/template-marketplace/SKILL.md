---
name: template-marketplace
description: Pre-built project templates for common app types. Scaffolds complete projects instantly.
---

# Template Marketplace

## Purpose
Provides **ready-made project templates** for common application types. Instead of starting from zero, users pick a template and get a complete project structure with best practices built in.

## Usage

```bash
# List all available templates:
python .agent/skills/template-marketplace/scripts/template_engine.py --action list

# Show details of a specific template:
python .agent/skills/template-marketplace/scripts/template_engine.py --action show --template saas

# Generate project structure from template:
python .agent/skills/template-marketplace/scripts/template_engine.py --action generate --template saas --name "MyApp"

# Search templates by keyword:
python .agent/skills/template-marketplace/scripts/template_engine.py --action search --query "e-commerce"
```

## Available Templates
- **SaaS Starter**: Multi-tenant SaaS with auth, billing, dashboard
- **E-Commerce**: Product catalog, cart, checkout, payment integration
- **Blog/CMS**: Content management, markdown, categories, SEO
- **API Service**: REST API with auth, rate limiting, documentation
- **Landing Page**: Marketing page with hero, features, pricing, CTA
- **Dashboard**: Admin panel with charts, tables, user management
- **Mobile App**: React Native/Expo with navigation, auth, API

## Integration
- Used by `@[/quickstart]` to auto-select the best template based on user's idea.
- Used by `@[/leader]` during Step 1 to suggest starting points.
- Integrates with `project-scaffolder` for enhanced structure.
