# Frontend Developer - Component, Layout, State Management (React/Vue/Tailwind).

# Frontend Developer Workflow

## Core Principles
1.  **Vibe First**: Always check `design-system/luxe-shop/MASTER.md` (or run `ui-ux-pro-max`) before writing CSS.
2.  **Token Saver**: Never ask LLM to rewrite a whole file. Use `diff-applier`.
3.  **Clean Code**: Standard ESLint/Prettier rules apply.

## Workflow

### Track 1: Modern Frameworks (React/Vue)
*For: Web Apps, Dashboards, Complex Logic*
1.  **Scaffold**: `python .agent/skills/project-scaffolder/scripts/scaffold.py --stack nextjs`
2.  **Context**: `python .agent/skills/context-manager/scripts/minify.py src/App.tsx`
3.  **Component Gen**: Use `ui-ux-pro-max` for Tailwind components.

### Track 2: Vanilla Web (HTML/CSS/JS)
*For: Landing Pages, Simple Sites, Old School Cool*
1.  **Scaffold**: 
    ```bash
    python .agent/skills/project-scaffolder/scripts/scaffold.py --stack html-css-js --name "MySite"
    ```
2.  **Style System**:
    - Use `ui-ux-pro-max` to generate `variables.css`.
    - `python .agent/skills/ui-ux-pro-max/scripts/design_system.py --query "Modern Dark" --format css > css/variables.css`
3.  **Implementation**:
    - Ask LLM: "Write HTML structure for index.html using variables from css/variables.css".
    - Apply with `diff-applier`.

### Step 1: Context Loading (Cheap)
Don't read the whole `App.tsx`. Minify it first to see structure.
```bash
python .agent/skills/context-manager/scripts/minify.py src/App.tsx
```

### Step 2: Component Generation
Use `ui-ux-pro-max` context to generate components that match the design system.
```bash
# Example: Generate a Navbar
"Generate a Navbar component matching the project style in .agent/project_context.json"
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
