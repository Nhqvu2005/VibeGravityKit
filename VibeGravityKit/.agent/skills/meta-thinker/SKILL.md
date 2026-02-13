---
name: meta-thinker
description: Creative idea advisor. Brainstorm frameworks, product archetypes, industry data, and monetization models. Zero-token data retrieval via script.
---

# Meta Thinker Skill

## Overview
Provides rich data for brainstorming and idea development.
Instead of consuming tokens to "think", the agent uses a script to retrieve existing data.

## Data Files

| File | Content | Entries |
| :--- | :--- | :---: |
| `data/brainstorm_frameworks.json` | 15 creative frameworks (SCAMPER, Lean Canvas, TRIZ, Disney...) | 15 |
| `data/product_archetypes.json` | 25 product templates + examples | 25 |
| `data/industry_database.json` | 45 industries + pain points + opportunities | 45 |
| `data/feature_ideas.json` | 300+ feature ideas by 23 categories | 300+ |
| `data/monetization_models.json` | 16 monetization models + examples | 16 |
| `data/platform_guide.json` | 6 platforms + pros/cons + tech stacks | 6 |

## Script Usage

```bash
# Find ideas by domain
python scripts/idea_engine.py --domain "food-delivery" --query "healthy"

# Get features for a product type
python scripts/idea_engine.py --archetype "marketplace" --platform "mobile"

# Find suitable monetization
python scripts/idea_engine.py --monetization --domain "education"

# Brainstorm with a framework
python scripts/idea_engine.py --framework "lean-canvas" --context "fitness app"
```

## Output
The script returns compact JSON, the agent just needs to read it and present it to the user.
Saves ~90% tokens compared to self-brainstorming without data.
