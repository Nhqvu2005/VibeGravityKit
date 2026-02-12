#!/usr/bin/env python3
"""
Meta Thinker — Idea Engine (Zero-Token Data Retrieval)

Truy xuất data sáng tạo mà không tốn token. Agent gọi script này
để lấy keywords, trends, features, monetization models phù hợp.

Usage:
    python idea_engine.py --domain <domain> [--query <keywords>]
    python idea_engine.py --archetype <type> [--platform <platform>]
    python idea_engine.py --monetization [--domain <domain>]
    python idea_engine.py --framework <id>
    python idea_engine.py --features <category>
    python idea_engine.py --platform <id>
    python idea_engine.py --explore <free_text>
"""

import argparse
import json
import sys
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parent.parent / "data"


def load_json(filename):
    filepath = DATA_DIR / filename
    if not filepath.exists():
        print(f"Error: {filepath} not found")
        sys.exit(1)
    with open(filepath, "r", encoding="utf-8") as f:
        return json.load(f)


def search_industry(domain, query=None):
    """Tìm ngành + pain points + opportunities theo domain."""
    industries = load_json("industry_database.json")
    results = []
    keywords = domain.lower().replace("-", " ").replace("_", " ").split()

    for ind in industries:
        name_lower = ind["name"].lower()
        id_lower = ind["id"].lower()
        all_text = json.dumps(ind, ensure_ascii=False).lower()

        # Match by id, name, or content
        if any(kw in id_lower or kw in name_lower or kw in all_text for kw in keywords):
            result = {
                "industry": ind["name"],
                "pain_points": ind["pain_points"],
                "opportunities": ind["opportunities"],
                "trends": ind["trends"],
                "example_ideas": ind["example_ideas"]
            }
            # Filter by query if provided
            if query:
                query_lower = query.lower()
                result["matched_opportunities"] = [
                    o for o in ind["opportunities"] if query_lower in o.lower()
                ]
                result["matched_ideas"] = [
                    i for i in ind["example_ideas"] if query_lower in i.lower()
                ]
            results.append(result)

    if not results:
        # Fuzzy: search across all industries
        for ind in industries:
            all_text = json.dumps(ind, ensure_ascii=False).lower()
            if any(kw in all_text for kw in keywords):
                results.append({
                    "industry": ind["name"],
                    "pain_points": ind["pain_points"][:3],
                    "opportunities": ind["opportunities"][:3]
                })

    return results or [{"message": f"No industry found for '{domain}'. Available: " +
                        ", ".join(i["id"] for i in industries)}]


def search_archetype(archetype, platform=None):
    """Tìm product archetype + features + monetization."""
    archetypes = load_json("product_archetypes.json")
    results = []
    arch_lower = archetype.lower()

    for arch in archetypes:
        if arch_lower in arch["id"].lower() or arch_lower in arch["name"].lower():
            result = {
                "archetype": arch["name"],
                "description": arch["description"],
                "examples": arch["examples"],
                "core_features": arch["core_features"],
                "monetization": arch["monetization"],
                "complexity": arch["complexity"],
                "time_estimate": arch["time_estimate"]
            }
            if platform:
                result["platform_match"] = platform in arch.get("platforms", [])
            results.append(result)

    if platform and not results:
        # Filter by platform
        for arch in archetypes:
            if platform in arch.get("platforms", []):
                results.append({
                    "archetype": arch["name"],
                    "platforms": arch["platforms"],
                    "complexity": arch["complexity"]
                })

    return results or [{"message": f"No archetype found for '{archetype}'."}]


def search_monetization(domain=None):
    """Lấy monetization models, filter theo domain nếu có."""
    models = load_json("monetization_models.json")
    if not domain:
        return [{
            "id": m["id"],
            "name": m["name"],
            "description": m["description"],
            "best_for": m["best_for"],
            "examples": m["examples"][:3]
        } for m in models]

    # Filter relevant models
    results = []
    domain_lower = domain.lower()
    for m in models:
        best_for_str = json.dumps(m["best_for"], ensure_ascii=False).lower()
        if domain_lower in best_for_str or domain_lower in json.dumps(m["examples"]).lower():
            results.append({
                "name": m["name"],
                "how_it_works": m["how_it_works"],
                "pros": m["pros"],
                "pricing_tips": m["pricing_tips"]
            })

    return results or search_monetization()  # Fallback to all


def get_framework(framework_id):
    """Lấy chi tiết một brainstorm framework."""
    frameworks = load_json("brainstorm_frameworks.json")
    for f in frameworks:
        if framework_id.lower() in f["id"].lower() or framework_id.lower() in f["name"].lower():
            return f
    return {"message": f"Framework '{framework_id}' not found. Available: " +
            ", ".join(f["id"] for f in frameworks)}


def get_features(category=None):
    """Lấy feature ideas theo category."""
    features = load_json("feature_ideas.json")
    if category:
        cat_lower = category.lower().replace("-", "_").replace(" ", "_")
        for key, values in features.items():
            if cat_lower in key.lower():
                return {key: values}
        return {"message": f"Category '{category}' not found. Available: " +
                ", ".join(features.keys())}
    # Return all categories with counts
    return {k: f"{len(v)} features" for k, v in features.items()}


def get_platform(platform_id):
    """Lấy platform guide chi tiết."""
    platforms = load_json("platform_guide.json")
    for p in platforms:
        if platform_id.lower() in p["id"].lower() or platform_id.lower() in p["name"].lower():
            return p
    return {"message": f"Platform '{platform_id}' not found. Available: " +
            ", ".join(p["id"] for p in platforms)}


def explore(text):
    """Tìm kiếm tự do across tất cả data files."""
    text_lower = text.lower()
    results = {"industries": [], "archetypes": [], "features": [], "monetization": []}

    # Search industries
    for ind in load_json("industry_database.json"):
        if text_lower in json.dumps(ind, ensure_ascii=False).lower():
            results["industries"].append(ind["name"])

    # Search archetypes
    for arch in load_json("product_archetypes.json"):
        if text_lower in json.dumps(arch, ensure_ascii=False).lower():
            results["archetypes"].append(arch["name"])

    # Search features
    features = load_json("feature_ideas.json")
    for cat, items in features.items():
        matched = [i for i in items if text_lower in i.lower()]
        if matched:
            results["features"].extend(matched[:5])

    # Search monetization
    for m in load_json("monetization_models.json"):
        if text_lower in json.dumps(m, ensure_ascii=False).lower():
            results["monetization"].append(m["name"])

    # Clean empty
    results = {k: v for k, v in results.items() if v}
    return results or {"message": f"No results for '{text}'"}


def main():
    parser = argparse.ArgumentParser(
        description="Meta Thinker Idea Engine — Zero-Token Data Retrieval"
    )
    parser.add_argument("--domain", help="Industry/domain to search (e.g. food, finance, education)")
    parser.add_argument("--query", help="Additional keywords to filter")
    parser.add_argument("--archetype", help="Product archetype (e.g. saas, marketplace, utility)")
    parser.add_argument("--monetization", action="store_true", help="List monetization models")
    parser.add_argument("--framework", help="Brainstorm framework ID (e.g. scamper, lean-canvas)")
    parser.add_argument("--features", help="Feature category (e.g. auth, payment, ai)")
    parser.add_argument("--platform", help="Platform guide (e.g. web, mobile, desktop)")
    parser.add_argument("--explore", help="Free-text search across all data")

    args = parser.parse_args()

    if args.domain:
        result = search_industry(args.domain, args.query)
    elif args.archetype:
        result = search_archetype(args.archetype, args.platform)
    elif args.monetization:
        result = search_monetization(args.domain)
    elif args.framework:
        result = get_framework(args.framework)
    elif args.features is not None:
        result = get_features(args.features if args.features else None)
    elif args.platform:
        result = get_platform(args.platform)
    elif args.explore:
        result = explore(args.explore)
    else:
        parser.print_help()
        return

    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
