---
name: release-manager
description: Changelog generation, version bumping, and release automation.
---

# Release Manager Skill

## Purpose
Automates version management: reads git history, generates changelogs, bumps versions, and prepares releases — all without manual work.

## Usage

```bash
# Generate changelog:
python .agent/skills/release-manager/scripts/release.py --action changelog

# Changelog since tag:
python .agent/skills/release-manager/scripts/release.py --action changelog --since "v2.0.0"

# Bump version (patch/minor/major):
python .agent/skills/release-manager/scripts/release.py --action bump --type minor

# Show current version:
python .agent/skills/release-manager/scripts/release.py --action version
```

## Output
- `changelog`: Grouped commit list (feat/fix/chore/docs)
- `bump`: Updates VERSION file and outputs new version
- `version`: Shows current version from VERSION file
