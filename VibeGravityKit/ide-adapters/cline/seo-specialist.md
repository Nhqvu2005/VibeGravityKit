---
description: SEO Specialist - Search Engine Optimization.
---

# SEO Specialist Workflow

## Core Principles
1.  **Technical SEO**: Clean HTML structure, fast load times.
2.  **Content Strategy**: Keywords from `market-trend-analyst`.
3.  **Zero Token Analysis**: Use regex scripts first.

## Workflow

### Step 1: Keyword Research
Use Market Trend Analyst (Batch 1).
```bash
python .agent/skills/market-trend-analyst/scripts/trend_report.py --niche "E-commerce"
```

### Step 2: Audit Pages
Check for missing meta tags/alt text.
```bash
python .agent/skills/seo-analyzer/scripts/seo_check.py src/app/page.tsx
```

### Step 3: Optimize
Update tags using `diff-applier`.
