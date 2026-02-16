---
name: i18n-manager
description: Extracts hardcoded strings from your code for internationalization. Generates translation files.
---

# I18n Manager

Scans your project for hardcoded user-facing strings and extracts them into translation files for internationalization.

## Usage

```bash
python .agent/skills/i18n-manager/scripts/string_extractor.py --path "src/" --output "locales/"
```

### What It Does

1. Scans source files for hardcoded strings (JSX text, template literals, Python f-strings)
2. Generates `en.json` translation file with extracted strings
3. Creates translation keys automatically (e.g., `"Welcome to our app"` → `welcome_to_our_app`)
4. Reports files and line numbers for each extracted string

## Data

- `data/i18n_patterns.json` — Detection patterns and common translation structures

## Supported Frameworks

- React/Next.js (JSX text content)
- Vue.js (template text)
- Python (user-facing strings)
- HTML templates
