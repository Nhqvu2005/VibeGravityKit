---
name: color-palette-generator
description: Generates standard Color Palettes for UI design.
---

# Color Palette Generator

## Purpose
Provides pre-mixed, UX/UI standard color palettes in various styles (Modern, Corporate, Dark Mode...).

## Usage

### 1. Generate Palette
```bash
python .agent/skills/color-palette-generator/scripts/palette.py --style modern
```

### Supported Styles
- `modern`: Bright, common for SaaS/Startup (Blue/Green)
- `corporate`: Formal, trustworthy (Navy/Grey)
- `playful`: Fun, dynamic (Pink/Purple/Yellow)
- `dark_tech`: Dark mode, futuristic (Indigo/Neon)
- `luxury`: Elegant (Gold/Black)

### Output
Script returns Hex codes and CSS Variables ready-to-copy.
