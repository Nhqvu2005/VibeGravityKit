#!/usr/bin/env python3
"""
Context Router — Universal data query router for all skills.

Searches across skill data files and returns only matching entries,
dramatically reducing token consumption.

Usage:
    python context_router.py --query "fintech"
    python context_router.py --skill meta-thinker --query "SCAMPER"
    python context_router.py --skill meta-thinker --source industry_database --id fintech
    python context_router.py --list
"""

import argparse
import json
import os
import sys

SKILLS_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "..")


def discover_data_sources(skills_dir):
    """Find all JSON data files across all skills."""
    sources = {}
    skills_path = os.path.join(skills_dir, "skills")
    if not os.path.isdir(skills_path):
        return sources

    for skill_name in sorted(os.listdir(skills_path)):
        data_dir = os.path.join(skills_path, skill_name, "data")
        if not os.path.isdir(data_dir):
            continue
        for fname in sorted(os.listdir(data_dir)):
            if fname.endswith(".json"):
                source_name = fname.replace(".json", "")
                key = f"{skill_name}/{source_name}"
                sources[key] = os.path.join(data_dir, fname)
    return sources


def load_json(filepath):
    """Load a JSON file safely."""
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, FileNotFoundError):
        return None


def search_in_value(value, query):
    """Recursively check if query appears in a JSON value."""
    query_lower = query.lower()
    if isinstance(value, str):
        return query_lower in value.lower()
    elif isinstance(value, list):
        return any(search_in_value(item, query) for item in value)
    elif isinstance(value, dict):
        return any(search_in_value(v, query) for v in value.values())
    return False


def search_data(data, query):
    """Search within a JSON data structure and return matching entries."""
    results = []

    if isinstance(data, list):
        for item in data:
            if search_in_value(item, query):
                results.append(item)
    elif isinstance(data, dict):
        for key, value in data.items():
            if search_in_value(key, query) or search_in_value(value, query):
                results.append({key: value})
    return results


def get_by_id(data, item_id):
    """Get a specific item by its 'id' field."""
    if isinstance(data, list):
        for item in data:
            if isinstance(item, dict) and item.get("id") == item_id:
                return item
    elif isinstance(data, dict):
        if item_id in data:
            return {item_id: data[item_id]}
    return None


def list_sources(sources):
    """Print all available data sources."""
    print("📂 Available Data Sources:")
    print(f"{'Source':<45} {'File'}")
    print("-" * 80)
    current_skill = ""
    for key, path in sorted(sources.items()):
        skill = key.split("/")[0]
        if skill != current_skill:
            current_skill = skill
            print(f"\n  [{skill}]")
        source = key.split("/")[1]
        size = os.path.getsize(path)
        print(f"    {source:<40} ({size:,} bytes)")
    print(f"\nTotal: {len(sources)} data sources")


def main():
    parser = argparse.ArgumentParser(description="Smart Context Router — Query skill data efficiently")
    parser.add_argument("--query", "-q", help="Search query (keyword)")
    parser.add_argument("--skill", "-s", help="Filter by skill name")
    parser.add_argument("--source", help="Specific data source name (without .json)")
    parser.add_argument("--id", help="Get specific item by ID")
    parser.add_argument("--list", "-l", action="store_true", help="List all data sources")
    parser.add_argument("--max-results", type=int, default=5, help="Max results per source (default: 5)")
    parser.add_argument("--compact", action="store_true", help="Compact JSON output (no indentation)")

    args = parser.parse_args()

    # Resolve skills directory
    agent_dir = SKILLS_DIR
    if not os.path.isdir(os.path.join(agent_dir, "skills")):
        # Try from .agent directory
        agent_dir = os.path.join(os.getcwd(), ".agent")
        if not os.path.isdir(os.path.join(agent_dir, "skills")):
            print("Error: Cannot find .agent/skills/ directory.", file=sys.stderr)
            sys.exit(1)

    sources = discover_data_sources(agent_dir)

    if args.list:
        list_sources(sources)
        return

    if not args.query and not args.id:
        parser.print_help()
        return

    # Filter sources
    filtered = {}
    for key, path in sources.items():
        skill_name = key.split("/")[0]
        source_name = key.split("/")[1]
        if args.skill and skill_name != args.skill:
            continue
        if args.source and source_name != args.source:
            continue
        filtered[key] = path

    if not filtered:
        print(f"No data sources found matching filters.", file=sys.stderr)
        sys.exit(1)

    # Search or get by ID
    indent = None if args.compact else 2
    total_results = 0

    for key, path in sorted(filtered.items()):
        data = load_json(path)
        if data is None:
            continue

        if args.id:
            result = get_by_id(data, args.id)
            if result:
                print(f"\n🎯 [{key}] ID: {args.id}")
                print(json.dumps(result, indent=indent, ensure_ascii=False))
                total_results += 1
        elif args.query:
            results = search_data(data, args.query)
            if results:
                shown = results[:args.max_results]
                print(f"\n🔍 [{key}] {len(results)} match(es)" +
                      (f" (showing top {args.max_results})" if len(results) > args.max_results else ""))
                print(json.dumps(shown, indent=indent, ensure_ascii=False))
                total_results += len(results)

    if total_results == 0:
        target = args.id or args.query
        print(f"No results found for: '{target}'")
    else:
        print(f"\n📊 Total: {total_results} result(s)")


if __name__ == "__main__":
    main()
