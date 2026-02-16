#!/usr/bin/env python3
"""
Tech Stack Advisor — Compare and Recommend Technologies.

Usage:
    python advisor.py --category web --keywords "seo,fast"
    python advisor.py --compare --category frontend
    python advisor.py --list
    python advisor.py --category ai_ml --keywords "rag,enterprise"
"""

import argparse
import json
from pathlib import Path

DATA_FILE = Path(__file__).parent.parent / "data" / "tech_data.json"
STACKS_FILE = Path(__file__).parent.parent / "data" / "stacks.json"

def load_data():
    if not DATA_FILE.exists():
        return {}
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def load_stacks():
    if not STACKS_FILE.exists():
        return []
    with open(STACKS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def list_categories():
    """List all available categories and their tech count."""
    data = load_data()
    stacks = load_stacks()

    print("\n" + "=" * 60)
    print("📂 AVAILABLE CATEGORIES")
    print("=" * 60)

    cats = data.get("categories", {})
    for cat, items in cats.items():
        print(f"  {cat:<15} — {len(items)} technologies")

    # Count stacks by category
    stack_cats = {}
    for s in stacks:
        c = s.get("category", "other")
        stack_cats[c] = stack_cats.get(c, 0) + 1

    print(f"\n📦 FULL-STACK COMBOS: {len(stacks)} total")
    for c, count in sorted(stack_cats.items()):
        print(f"  {c:<15} — {count} stacks")

    print("\n" + "=" * 60 + "\n")

def recommend(category, keywords):
    data = load_data()

    print("\n" + "=" * 60)
    print(f"🤖 TECH RECOMMENDATION: {category.upper()}")
    print(f"   Keywords: {keywords}")
    print("=" * 60)

    # Map 'web' to multiple categories
    cat_map = {
        "web": ["frontend", "backend", "database"],
        "fullstack": ["frontend", "backend", "database", "devops"],
        "all": list(data.get("categories", {}).keys())
    }

    categories = cat_map.get(category, [category])
    found = False

    for cat in categories:
        options = data.get("categories", {}).get(cat, {})
        if not options:
            continue

        found = True
        print(f"\n📂 {cat.upper()} ({len(options)} options):")

        # Score each option by keyword match
        scored = []
        for key, info in options.items():
            score = 0
            text = " ".join([
                info.get("description", ""),
                " ".join(info.get("pros", [])),
                " ".join(info.get("use_cases", [])),
                info.get("type", "")
            ]).lower()

            for k in keywords.lower().split(","):
                k = k.strip()
                if k and k in text:
                    score += 1

            scored.append((score, info))

        scored.sort(key=lambda x: (-x[0], -x[1].get("popularity", 0)))

        for score, info in scored[:3]:
            marker = "⭐" if score > 0 else "  "
            print(f"   {marker} {info['name']} (match: {score}, pop: {info.get('popularity', '?')})")
            print(f"      {info.get('description', '')}")
            if info.get("use_cases"):
                print(f"      Best for: {', '.join(info['use_cases'][:3])}")

    if not found:
        cats = list(data.get("categories", {}).keys())
        print(f"\n⚠️  Category '{category}' not found.")
        print(f"   Available: {', '.join(cats)}")
        print(f"   Or use: web, fullstack, all")

    print("\n" + "=" * 60 + "\n")

def recommend_stack(keywords):
    """Recommend full-stack combos from stacks.json."""
    stacks = load_stacks()

    print("\n" + "=" * 60)
    print(f"📦 STACK RECOMMENDATION")
    print(f"   Keywords: {keywords}")
    print("=" * 60)

    scored = []
    for stack in stacks:
        score = 0
        text = " ".join([
            stack.get("name", ""),
            " ".join(stack.get("tags", [])),
            stack.get("best_for", ""),
            " ".join(stack.get("pros", []))
        ]).lower()

        for k in keywords.lower().split(","):
            k = k.strip()
            if k and k in text:
                score += 1

        if score > 0:
            scored.append((score, stack))

    scored.sort(key=lambda x: x[0], reverse=True)

    if not scored:
        print("\n⚠️  No matching stacks found. Try different keywords.")
    else:
        for score, s in scored[:5]:
            print(f"\n⭐ {s['name']} (match: {score})")
            print(f"   Category: {s.get('category', '?')}")
            comps = s.get("components", {})
            for k, v in comps.items():
                print(f"   {k}: {v}")
            print(f"   Best for: {s.get('best_for', '?')}")

    print("\n" + "=" * 60 + "\n")

def compare(category):
    data = load_data()

    print("\n" + "=" * 60)
    print(f"⚖️  TECH COMPARISON: {category.upper()}")
    print("=" * 60)

    options = data.get("categories", {}).get(category, {})

    if not options:
        cats = list(data.get("categories", {}).keys())
        print(f"\n⚠️  Category '{category}' not found.")
        print(f"   Available: {', '.join(cats)}")
    else:
        for key, info in options.items():
            print(f"\n🔹 {info['name']} ({info.get('type', '-')})")
            print(f"   ✅ Pros: {', '.join(info.get('pros', []))}")
            print(f"   ❌ Cons: {', '.join(info.get('cons', []))}")
            print(f"   💡 Best for: {', '.join(info.get('use_cases', []))}")
            print(f"   📊 Popularity: {info.get('popularity', '?')}")

    print("\n" + "=" * 60 + "\n")

def main():
    parser = argparse.ArgumentParser(description="Tech Stack Advisor")
    parser.add_argument("--category", "-c", type=str, help="Category: frontend, backend, database, mobile, devops, ai_ml, auth, testing, messaging, cms, web, fullstack, all")
    parser.add_argument("--keywords", "-k", type=str, default="", help="Comma-separated keywords for scoring")
    parser.add_argument("--compare", action="store_true", help="Show comparison view for a category")
    parser.add_argument("--stack", "-s", action="store_true", help="Recommend full-stack combos (searches stacks.json)")
    parser.add_argument("--list", "-l", action="store_true", help="List all available categories")
    parser.add_argument("--json", "-j", action="store_true", help="Output raw JSON")

    args = parser.parse_args()

    if args.list:
        list_categories()
    elif args.stack:
        if not args.keywords:
            print("⚠️  Use --keywords with --stack. Example: --stack --keywords 'seo,react'")
        else:
            recommend_stack(args.keywords)
    elif args.compare:
        if not args.category:
            print("⚠️  Use --category with --compare. Example: --compare --category frontend")
        else:
            compare(args.category)
    elif args.category:
        recommend(args.category, args.keywords)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
