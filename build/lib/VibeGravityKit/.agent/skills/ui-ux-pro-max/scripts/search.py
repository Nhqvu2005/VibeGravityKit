#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
UI/UX Pro Max Search - BM25 search engine for UI/UX style guides
Usage: python search.py "<query>" [--domain <domain>] [--stack <stack>] [--max-results 3]
       python search.py "<query>" --design-system [-p "Project Name"]
       python search.py "<query>" --design-system --persist [-p "Project Name"] [--page "dashboard"]

Domains: style, prompt, color, chart, landing, product, ux, typography
Stacks: html-tailwind, react, nextjs

Persistence (Master + Overrides pattern):
  --persist    Save design system to design-system/MASTER.md
  --page       Also create a page-specific override file in design-system/pages/
"""

import argparse
import sys
import io
import os
from core import CSV_CONFIG, AVAILABLE_STACKS, MAX_RESULTS, search, search_stack
from design_system import generate_design_system, persist_design_system

# Force UTF-8 for stdout/stderr to handle emojis on Windows (cp1252 default)
if sys.stdout.encoding and sys.stdout.encoding.lower() != 'utf-8':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
if sys.stderr.encoding and sys.stderr.encoding.lower() != 'utf-8':
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')


def format_output(result):
    """Format results for Claude consumption (token-optimized)"""
    if "error" in result:
        return f"Error: {result['error']}"

    output = []
    if result.get("stack"):
        output.append(f"## UI Pro Max Stack Guidelines")
        output.append(f"**Stack:** {result['stack']} | **Query:** {result['query']}")
    else:
        output.append(f"## UI Pro Max Search Results")
        output.append(f"**Domain:** {result['domain']} | **Query:** {result['query']}")
    output.append(f"**Source:** {result['file']} | **Found:** {result['count']} results\n")

    for i, row in enumerate(result['results'], 1):
        output.append(f"### Result {i}")
        for key, value in row.items():
            value_str = str(value)
            if len(value_str) > 300:
                value_str = value_str[:300] + "..."
            output.append(f"- **{key}:** {value_str}")
        output.append("")

    return "\n".join(output)



CONTEXT_FILE = ".agent/project_context.json"

def save_context(args):
    """Save current arguments to context file."""
    import json
    context = {}
    if args.project_name: context["project_name"] = args.project_name
    if args.query: context["last_query"] = args.query
    
    with open(CONTEXT_FILE, "w", encoding="utf-8") as f:
        json.dump(context, f, indent=2)
    print(f"💾 Context saved to {CONTEXT_FILE}")

def load_context():
    """Load arguments from context file."""
    import json
    if not os.path.exists(CONTEXT_FILE):
        return {}
    try:
        with open(CONTEXT_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return {}

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="UI Pro Max Search")
    parser.add_argument("query", nargs="?", help="Search query")
    parser.add_argument("--domain", "-d", choices=list(CSV_CONFIG.keys()), help="Search domain")
    parser.add_argument("--stack", "-s", choices=AVAILABLE_STACKS, help="Stack-specific search")
    parser.add_argument("--max-results", "-n", type=int, default=MAX_RESULTS, help="Max results")
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    
    # Design system
    parser.add_argument("--design-system", "-ds", action="store_true", help="Generate design system")
    parser.add_argument("--project-name", "-p", type=str, default=None, help="Project name")
    parser.add_argument("--format", "-f", choices=["ascii", "markdown"], default="ascii", help="Output format")
    
    # Persistence
    parser.add_argument("--persist", action="store_true", help="Save to design-system/MASTER.md")
    parser.add_argument("--page", type=str, default=None, help="Page override")
    parser.add_argument("--output-dir", "-o", type=str, default=None, help="Output directory")
    
    # Context
    parser.add_argument("--save-context", action="store_true", help="Save args to project context")
    parser.add_argument("--load-context", action="store_true", help="Load args from project context")

    args = parser.parse_args()

    # Load context if requested
    if args.load_context:
        context = load_context()
        if not args.project_name and "project_name" in context:
            args.project_name = context["project_name"]
            print(f"📂 Loaded project: {args.project_name}")
        if not args.query and "last_query" in context:
            args.query = context["last_query"]
            print(f"🔎 Loaded query: {args.query}")

    if not args.query:
        print("Error: query required (or use --load-context)")
        sys.exit(1)

    # Save context if requested
    if args.save_context:
        save_context(args)

    # Design system takes priority
    if args.design_system:
        result = generate_design_system(
            args.query, 
            args.project_name, 
            args.format,
            persist=args.persist,
            page=args.page,
            output_dir=args.output_dir
        )
        print(result)
        
        if args.persist:
            project_slug = args.project_name.lower().replace(' ', '-') if args.project_name else "default"
            print("\n" + "=" * 60)
            print(f"✅ Design system persisted to design-system/{project_slug}/")
            print(f"   📄 MASTERT.md")
            print(f"   🎨 tailwind.config.js (Auto-generated)")
            if args.page:
                print(f"   📄 pages/{args.page}.md")
            print("=" * 60)

    # Stack search
    elif args.stack:
        result = search_stack(args.query, args.stack, args.max_results)
        if args.json:
            import json
            print(json.dumps(result, indent=2, ensure_ascii=False))
        else:
            print(format_output(result))
    # Domain search
    else:
        result = search(args.query, args.domain, args.max_results)
        if args.json:
            import json
            print(json.dumps(result, indent=2, ensure_ascii=False))
        else:
            print(format_output(result))

