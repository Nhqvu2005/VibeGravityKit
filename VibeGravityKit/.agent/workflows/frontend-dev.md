---
description: Frontend Developer - Component, Layout, State Management (React/Vue/Tailwind).
---

# Frontend Developer Workflow

> ⚠️ **MANDATORY**: Read this ENTIRE file before starting work.
> Follow the steps IN ORDER. Read the SKILL.md for each skill before using it.
> Also read `.agent/brain/phase_context.md` for project context.

## Core Principles
1. **Design Contract First**: ALWAYS read `design_contract.md` BEFORE writing any CSS/styling.
2. **Token Saver**: Never ask LLM to rewrite a whole file. Use `diff-applier`.
3. **Clean Code**: Standard ESLint/Prettier rules apply.

## Workflow

### Step 0: Read Design Contract (MANDATORY)

> ⚠️ This step is NOT optional. Skip it = wrong styling.

1. **Read** `.agent/brain/phase_context.md` — understand project stack and constraints.
2. **Check** if `.agent/brain/design_contract.md` exists:
   - **YES** → Read it. Apply ALL colors, fonts, component rules, spacing, effects.
     Do NOT use default/generic styling. Every color and font must come from this file.
   - **NO** → Run ui-ux-pro-max to generate one:
     ```bash
     python .agent/skills/ui-ux-pro-max/scripts/search.py "<product> modern" --design-system -p "<Project>"
     ```
     Then save the output as `.agent/brain/design_contract.md`.

### Step 1: Context Loading (Cheap)
Don't read the whole `App.tsx`. Minify it first to see structure.
```bash
python .agent/skills/context-manager/scripts/minify.py src/App.tsx
```

### Track A: Modern Frameworks (React/Vue)
*For: Web Apps, Dashboards, Complex Logic*
1. **Scaffold**: `python .agent/skills/project-scaffolder/scripts/scaffold.py --stack nextjs`
2. **Read** `.agent/skills/ui-ux-pro-max/SKILL.md` (view_file)
3. **Apply design contract** — use the colors, fonts, and rules from `design_contract.md`

### Track B: Vanilla Web (HTML/CSS/JS)
*For: Landing Pages, Simple Sites*
1. **Scaffold**:
    ```bash
    python .agent/skills/project-scaffolder/scripts/scaffold.py --stack html-css-js --name "MySite"
    ```
2. **Apply design contract** — implement CSS variables from `design_contract.md`:
   ```css
   :root {
     --color-primary: /* from design_contract.md */;
     --color-secondary: /* from design_contract.md */;
     --font-heading: /* from design_contract.md */;
     --font-body: /* from design_contract.md */;
   }
   ```

### Step 2: Component Generation
**First**: Read `.agent/skills/ui-ux-pro-max/SKILL.md` (view_file)
**Then**: Generate components that match the design contract:
```bash
python .agent/skills/ui-ux-pro-max/scripts/search.py "<component> <style>" --format css
```

### Step 3: Implementation (Diff Only)
Ask LLM to output only the `SEARCH/REPLACE` block.
```python
<<<<<<< SEARCH
<div className="old-nav">
=======
<div className="new-nav variant-primary">
>>>>>>> REPLACE
```
Save to `patch.txt` and apply:
```bash
python .agent/skills/diff-applier/scripts/apply_patch.py src/components/Navbar.tsx patch.txt
```

### Step 4: Commit
```bash
python .agent/skills/git-manager/scripts/commit.py --type feat --scope ui --msg "Add Navbar component"
```

## Bug Fix Mode
When receiving a scoped bug fix from leader/QA:
1. Read the bug description carefully — note the exact file and line.
2. ONLY modify the specified file.
3. Do NOT refactor or change unrelated code.
4. Verify the fix matches the expected behavior.
