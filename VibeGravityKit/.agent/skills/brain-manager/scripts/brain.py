#!/usr/bin/env python3
"""
brain.py — Manage project brain (context, decisions, conventions).
"""

import json
import sys
import argparse
from pathlib import Path
from datetime import datetime

BRAIN_DIR = Path.cwd() / ".agent" / "brain"
CONTEXT_FILE = BRAIN_DIR / "project_context.json"
DECISIONS_FILE = BRAIN_DIR / "decisions.jsonl"
CONVENTIONS_FILE = BRAIN_DIR / "conventions.md"


def ensure_brain():
    """Ensure brain directory and files exist."""
    BRAIN_DIR.mkdir(parents=True, exist_ok=True)

    if not CONTEXT_FILE.exists():
        default_context = {
            "project": {
                "name": Path.cwd().name,
                "description": "",
                "tech_stack": [],
                "repo_url": "",
                "created_at": datetime.now().isoformat()
            },
            "architecture": {
                "pattern": "",
                "database": "",
                "api_style": "",
                "auth_method": "",
                "hosting": "",
                "notes": []
            },
            "conventions": {
                "naming": "",
                "file_structure": "",
                "git_branch_strategy": "",
                "commit_format": "",
                "code_style": ""
            },
            "known_issues": [],
            "current_sprint": {
                "goal": "",
                "status": "",
                "tasks": []
            }
        }
        CONTEXT_FILE.write_text(json.dumps(default_context, indent=2, ensure_ascii=False), encoding='utf-8')

    if not DECISIONS_FILE.exists():
        DECISIONS_FILE.touch()

    if not CONVENTIONS_FILE.exists():
        CONVENTIONS_FILE.write_text(
            "# Project Conventions\n\n"
            "## Naming\n\n## File Structure\n\n## Code Style\n\n## Git\n\n",
            encoding='utf-8'
        )


def cmd_show(args):
    """Show current project context."""
    ensure_brain()

    print("🧠 Project Brain\n")

    # Show context
    ctx = json.loads(CONTEXT_FILE.read_text(encoding='utf-8'))
    project = ctx.get("project", {})
    print(f"📦 Project: {project.get('name', 'Unknown')}")
    print(f"   Description: {project.get('description', '(not set)')}")
    if project.get('tech_stack'):
        print(f"   Tech Stack: {', '.join(project['tech_stack'])}")

    arch = ctx.get("architecture", {})
    if arch.get("pattern"):
        print(f"\n🏗️  Architecture: {arch['pattern']}")
    if arch.get("database"):
        print(f"   Database: {arch['database']}")
    if arch.get("api_style"):
        print(f"   API: {arch['api_style']}")

    # Show recent decisions
    if DECISIONS_FILE.exists() and DECISIONS_FILE.stat().st_size > 0:
        decisions = [json.loads(line) for line in DECISIONS_FILE.read_text(encoding='utf-8').strip().split('\n') if line.strip()]
        print(f"\n📋 Decisions ({len(decisions)} total):")
        for d in decisions[-5:]:  # Last 5
            print(f"   [{d.get('date', '?')}] {d.get('decision', '')}")
            if d.get('rationale'):
                print(f"      ↳ {d['rationale']}")

    # Known issues
    issues = ctx.get("known_issues", [])
    if issues:
        print(f"\n⚠️  Known Issues ({len(issues)}):")
        for issue in issues:
            print(f"   • {issue}")


def cmd_add_decision(args):
    """Add an architecture decision."""
    ensure_brain()

    decision = {
        "date": datetime.now().strftime("%Y-%m-%d"),
        "decision": args.decision,
        "rationale": args.rationale or "",
        "category": args.category or "general",
    }

    with open(DECISIONS_FILE, 'a', encoding='utf-8') as f:
        f.write(json.dumps(decision, ensure_ascii=False) + '\n')

    print(f"✅ Decision recorded: {args.decision}")


def cmd_set(args):
    """Set a project context value."""
    ensure_brain()

    ctx = json.loads(CONTEXT_FILE.read_text(encoding='utf-8'))

    # Navigate nested keys (e.g., "project.name")
    keys = args.key.split('.')
    obj = ctx
    for key in keys[:-1]:
        if key not in obj:
            obj[key] = {}
        obj = obj[key]

    # Handle list values
    value = args.value
    if ',' in value and keys[-1] in ('tech_stack', 'notes', 'known_issues', 'tasks'):
        value = [v.strip() for v in value.split(',')]

    obj[keys[-1]] = value
    CONTEXT_FILE.write_text(json.dumps(ctx, indent=2, ensure_ascii=False), encoding='utf-8')
    print(f"✅ Set {args.key} = {value}")


def cmd_export(args):
    """Export brain to a single JSON file."""
    ensure_brain()

    brain = {
        "context": json.loads(CONTEXT_FILE.read_text(encoding='utf-8')),
        "decisions": [],
        "conventions": "",
        "exported_at": datetime.now().isoformat(),
    }

    if DECISIONS_FILE.exists() and DECISIONS_FILE.stat().st_size > 0:
        brain["decisions"] = [
            json.loads(line) for line in DECISIONS_FILE.read_text(encoding='utf-8').strip().split('\n') if line.strip()
        ]

    if CONVENTIONS_FILE.exists():
        brain["conventions"] = CONVENTIONS_FILE.read_text(encoding='utf-8')

    output = Path(args.output)
    output.write_text(json.dumps(brain, indent=2, ensure_ascii=False), encoding='utf-8')
    print(f"✅ Brain exported to {output}")


def cmd_import(args):
    """Import brain from a JSON file."""
    ensure_brain()

    input_file = Path(args.input)
    if not input_file.exists():
        print(f"❌ File not found: {input_file}")
        return

    brain = json.loads(input_file.read_text(encoding='utf-8'))

    if "context" in brain:
        CONTEXT_FILE.write_text(json.dumps(brain["context"], indent=2, ensure_ascii=False), encoding='utf-8')

    if "decisions" in brain:
        with open(DECISIONS_FILE, 'w', encoding='utf-8') as f:
            for d in brain["decisions"]:
                f.write(json.dumps(d, ensure_ascii=False) + '\n')

    if "conventions" in brain:
        CONVENTIONS_FILE.write_text(brain["conventions"], encoding='utf-8')

    print(f"✅ Brain imported from {input_file}")


def main():
    parser = argparse.ArgumentParser(description='VibeGravityKit Brain Manager')
    subparsers = parser.add_subparsers(dest='command')

    # show
    subparsers.add_parser('show', help='Show project context')

    # add-decision
    add_dec = subparsers.add_parser('add-decision', help='Record an architecture decision')
    add_dec.add_argument('decision', help='The decision made')
    add_dec.add_argument('--rationale', '-r', help='Why this decision was made')
    add_dec.add_argument('--category', '-c', help='Category (e.g., database, auth, infra)')

    # set
    set_cmd = subparsers.add_parser('set', help='Set a project context value')
    set_cmd.add_argument('key', help='Dot-notation key (e.g., project.name)')
    set_cmd.add_argument('value', help='Value to set')

    # export
    export_cmd = subparsers.add_parser('export', help='Export brain to JSON')
    export_cmd.add_argument('--output', '-o', default='brain_export.json')

    # import
    import_cmd = subparsers.add_parser('import', help='Import brain from JSON')
    import_cmd.add_argument('--input', '-i', required=True)

    args = parser.parse_args()

    commands = {
        'show': cmd_show,
        'add-decision': cmd_add_decision,
        'set': cmd_set,
        'export': cmd_export,
        'import': cmd_import,
    }

    if args.command in commands:
        commands[args.command](args)
    else:
        parser.print_help()


if __name__ == '__main__':
    main()
