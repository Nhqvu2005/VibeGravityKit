#!/usr/bin/env python3
"""
generate_adapters.py — VibeGravityKit Multi-IDE Adapter Generator

Reads .agent/workflows/*.md and generates rule files for:
  - Cursor:   ide-adapters/cursor/*.mdc
  - Windsurf: ide-adapters/windsurf/*.md
  - Cline:    ide-adapters/cline/*.md
"""

import os
import re
from pathlib import Path

# Paths relative to this script (inside VibeGravityKit/)
PACKAGE_ROOT = Path(__file__).resolve().parent.parent
WORKFLOWS_DIR = PACKAGE_ROOT / ".agent" / "workflows"
ADAPTERS_DIR = PACKAGE_ROOT / "ide-adapters"


def parse_workflow(filepath: Path) -> dict:
    """Parse a workflow .md file into frontmatter and body."""
    content = filepath.read_text(encoding="utf-8")
    
    description = ""
    body = content
    
    # Extract YAML frontmatter
    fm_match = re.match(r"^---\s*\n(.*?)\n---\s*\n", content, re.DOTALL)
    if fm_match:
        frontmatter_text = fm_match.group(1)
        body = content[fm_match.end():]
        
        desc_match = re.search(r"description:\s*(.+)", frontmatter_text)
        if desc_match:
            description = desc_match.group(1).strip()
    
    return {
        "name": filepath.stem,
        "description": description,
        "body": body.strip(),
        "raw": content,
    }


def generate_cursor(workflow: dict, output_dir: Path):
    """Generate .mdc file for Cursor IDE."""
    output_dir.mkdir(parents=True, exist_ok=True)
    
    mdc_content = f"""---
description: {workflow['description']}
alwaysApply: true
---

{workflow['body']}
"""
    (output_dir / f"{workflow['name']}.mdc").write_text(mdc_content, encoding="utf-8")


def generate_windsurf(workflow: dict, output_dir: Path):
    """Generate .md file for Windsurf IDE."""
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Windsurf uses plain markdown, no special frontmatter needed
    ws_content = f"""# {workflow['description']}

{workflow['body']}
"""
    (output_dir / f"{workflow['name']}.md").write_text(ws_content, encoding="utf-8")


def generate_cline(workflow: dict, output_dir: Path):
    """Generate .md file for Cline IDE."""
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Cline supports same frontmatter format as our workflows
    cline_content = f"""---
description: {workflow['description']}
---

{workflow['body']}
"""
    (output_dir / f"{workflow['name']}.md").write_text(cline_content, encoding="utf-8")


def main():
    if not WORKFLOWS_DIR.exists():
        print(f"ERROR: Workflows directory not found: {WORKFLOWS_DIR}")
        return
    
    workflow_files = sorted(WORKFLOWS_DIR.glob("*.md"))
    if not workflow_files:
        print("ERROR: No workflow files found.")
        return
    
    print(f"Found {len(workflow_files)} workflow(s). Generating adapters...\n")
    
    cursor_dir = ADAPTERS_DIR / "cursor"
    windsurf_dir = ADAPTERS_DIR / "windsurf"
    cline_dir = ADAPTERS_DIR / "cline"
    
    for wf_path in workflow_files:
        workflow = parse_workflow(wf_path)
        
        generate_cursor(workflow, cursor_dir)
        generate_windsurf(workflow, windsurf_dir)
        generate_cline(workflow, cline_dir)
        
        print(f"  ✅ {workflow['name']}: cursor/.mdc, windsurf/.md, cline/.md")
    
    print(f"\n🎉 Generated adapters for {len(workflow_files)} agents in:")
    print(f"   {cursor_dir}")
    print(f"   {windsurf_dir}")
    print(f"   {cline_dir}")


if __name__ == "__main__":
    main()
