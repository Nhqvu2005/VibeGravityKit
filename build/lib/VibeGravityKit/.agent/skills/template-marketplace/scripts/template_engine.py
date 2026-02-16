#!/usr/bin/env python3
"""
Template Engine — Browse and generate project structures from templates.

Lists available templates, shows details, and generates project scaffolds
based on pre-defined best practices.

Usage:
    python template_engine.py --action list
    python template_engine.py --action show --template saas
    python template_engine.py --action generate --template saas --name "MyApp"
    python template_engine.py --action search --query "e-commerce"
"""

import argparse
import json
import os
import sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATES_FILE = os.path.join(SCRIPT_DIR, "..", "data", "templates.json")


def load_templates():
    """Load templates from JSON file."""
    with open(TEMPLATES_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data.get("templates", [])


def list_templates(templates):
    """Display all available templates."""
    print("📦 Available Project Templates")
    print("=" * 60)
    for t in templates:
        complexity_icon = {"low": "🟢", "medium": "🟡", "high": "🔴"}
        icon = complexity_icon.get(t["complexity"], "⚪")
        print(f"\n  {icon} {t['name']} [{t['id']}]")
        print(f"     {t['description']}")
        print(f"     Category: {t['category']} | Complexity: {t['complexity']}")
    print(f"\nTotal: {len(templates)} templates")
    print("Use --action show --template <id> for details")


def show_template(templates, template_id):
    """Show detailed info about a specific template."""
    template = next((t for t in templates if t["id"] == template_id), None)
    if not template:
        print(f"Template '{template_id}' not found.", file=sys.stderr)
        print(f"Available: {', '.join(t['id'] for t in templates)}")
        sys.exit(1)

    print(f"\n📦 {template['name']}")
    print(f"{'='*50}")
    print(f"Description: {template['description']}")
    print(f"Category: {template['category']}")
    print(f"Complexity: {template['complexity']}")

    print(f"\n🔧 Recommended Stack:")
    for key, value in template["recommended_stack"].items():
        print(f"  {key}: {value}")

    print(f"\n✨ Features ({len(template['features'])}):")
    for feature in template["features"]:
        print(f"  • {feature}")

    print(f"\n📂 Project Structure:")
    for folder, desc in template["structure"].items():
        print(f"  {folder:<30} {desc}")

    print(f"\n📄 Starter Files ({len(template['starter_files'])}):")
    for f in template["starter_files"]:
        print(f"  {f}")


def search_templates(templates, query):
    """Search templates by keyword."""
    query_lower = query.lower()
    results = []
    for t in templates:
        searchable = f"{t['name']} {t['description']} {' '.join(t['features'])} {t['category']}"
        if query_lower in searchable.lower():
            results.append(t)

    if not results:
        print(f"No templates found matching '{query}'")
        return

    print(f"🔍 Found {len(results)} template(s) matching '{query}':")
    for t in results:
        print(f"\n  📦 {t['name']} [{t['id']}]")
        print(f"     {t['description']}")


def generate_template(templates, template_id, project_name):
    """Generate project structure instructions from template."""
    template = next((t for t in templates if t["id"] == template_id), None)
    if not template:
        print(f"Template '{template_id}' not found.", file=sys.stderr)
        sys.exit(1)

    print(f"\n🚀 Project Generation Plan: {project_name}")
    print(f"{'='*50}")
    print(f"Template: {template['name']}")
    print(f"Stack: {json.dumps(template['recommended_stack'], indent=2)}")

    print(f"\n📂 Directories to create:")
    for folder in template["structure"]:
        full_path = os.path.join(project_name, folder)
        print(f"  mkdir -p {full_path}")

    print(f"\n📄 Files to create ({len(template['starter_files'])}):")
    for filepath in template["starter_files"]:
        full_path = os.path.join(project_name, filepath)
        print(f"  {full_path}")

    print(f"\n✨ Features to implement:")
    for i, feature in enumerate(template["features"], 1):
        print(f"  {i}. {feature}")

    print(f"\n💡 Next Steps:")
    print(f"  1. Create the project directory: mkdir {project_name}")
    print(f"  2. Use @[/architect] to design the database schema")
    print(f"  3. Use @[/designer] to create the design system")
    print(f"  4. Use @[/frontend-dev] and @[/backend-dev] to implement")


def main():
    parser = argparse.ArgumentParser(description="Template Marketplace — Project Templates")
    parser.add_argument("--action", "-a", required=True,
                        choices=["list", "show", "generate", "search"],
                        help="Action to perform")
    parser.add_argument("--template", "-t", help="Template ID")
    parser.add_argument("--name", "-n", default="my-project", help="Project name")
    parser.add_argument("--query", "-q", help="Search query")

    args = parser.parse_args()
    templates = load_templates()

    if args.action == "list":
        list_templates(templates)
    elif args.action == "show":
        if not args.template:
            print("Error: --template required for 'show' action", file=sys.stderr)
            sys.exit(1)
        show_template(templates, args.template)
    elif args.action == "generate":
        if not args.template:
            print("Error: --template required for 'generate' action", file=sys.stderr)
            sys.exit(1)
        generate_template(templates, args.template, args.name)
    elif args.action == "search":
        if not args.query:
            print("Error: --query required for 'search' action", file=sys.stderr)
            sys.exit(1)
        search_templates(templates, args.query)


if __name__ == "__main__":
    main()
