---
name: user-story-generator
description: Generates standard user stories with acceptance criteria from feature lists.
---

# User Story Generator

## Purpose
Converts raw feature ideas into formal User Stories (As a... I want to... So that...) with Acceptance Criteria (Given... When... Then...).

## Usage

### 1. Generate Stories
```bash
python .agent/skills/user-story-generator/scripts/generator.py --feature "Shopping Cart"
```

### Output
- Story 1: Add to cart
- Story 2: Remove from cart
- Story 3: View total price
- Acceptance Criteria for each.
