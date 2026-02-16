---
name: market-trend-analyst
description: Analyzes market trends, hot features, and user expectations.
---

# Market Trend Analyst

## Purpose
Identifies current market trends, performs web research, and analyzes "must-have" features for a specific domain.

## Tools

### 1. Web Search (DuckDuckGo — Zero Dependencies)

> **Uses only Python stdlib (urllib). No pip install. No API key.**

```bash
# Quick search
python .agent/skills/market-trend-analyst/scripts/web_search.py --query "best React frameworks 2025"

# JSON output
python .agent/skills/market-trend-analyst/scripts/web_search.py --query "NextJS vs Remix" --json

# Limit results
python .agent/skills/market-trend-analyst/scripts/web_search.py --query "AI SaaS trends" --max 5

# Save as Markdown report
python .agent/skills/market-trend-analyst/scripts/web_search.py --query "food delivery competitors" --output research.md

# Instant answer only (faster, no web scraping)
python .agent/skills/market-trend-analyst/scripts/web_search.py --query "Python datetime format" --instant-only
```

#### Output:
- **Instant Answer** — Direct answer from DuckDuckGo knowledge base
- **Abstract** — Summary from Wikipedia or other sources
- **Related Topics** — Related topics with URLs
- **Web Results** — Full web search results with titles, snippets, and URLs

### 2. Local Trend Database (Offline)

```bash
python .agent/skills/market-trend-analyst/scripts/trends.py --domain "ecommerce"
```

#### Output:
- Top 5 Trending Features
- Rising Technologies (AI, VR, etc.)
- User Expectations (Mobile-first, Dark mode)
- Declining Trends to avoid

Supported domains: ecommerce, saas, fintech, edtech, healthtech.
