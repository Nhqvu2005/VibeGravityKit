#!/usr/bin/env python3
"""
Task Estimator — Break down features into tasks, assign roles, and estimate effort.

Usage:
    python estimator.py --features "login,product listing,cart,checkout" --stack "nextjs-supabase"
"""

import argparse
import json
import sys

# === Mapping: feature → specific tasks ===
TASK_TEMPLATES = {
    "login": [
        {"task": "Design Login Page UI", "assignee": "🎨 Designer", "size": "S", "phase": "Design"},
        {"task": "Implement Login component", "assignee": "⚛️ Frontend Dev", "size": "M", "phase": "Frontend"},
        {"task": "API: POST /auth/login", "assignee": "⚙️ Backend Dev", "size": "M", "phase": "Backend"},
        {"task": "Setup auth middleware + session/JWT", "assignee": "⚙️ Backend Dev", "size": "M", "phase": "Backend"},
        {"task": "Test login flow (happy + error cases)", "assignee": "🧪 Tester", "size": "M", "phase": "Testing"},
    ],
    "register": [
        {"task": "Design Register Page UI", "assignee": "🎨 Designer", "size": "S", "phase": "Design"},
        {"task": "Implement Register page + form validation", "assignee": "⚛️ Frontend Dev", "size": "M", "phase": "Frontend"},
        {"task": "API: POST /auth/register + email verification", "assignee": "⚙️ Backend Dev", "size": "M", "phase": "Backend"},
        {"task": "DB: Create users table + migration", "assignee": "🏗️ Architect", "size": "S", "phase": "Setup"},
        {"task": "Test register flow", "assignee": "🧪 Tester", "size": "S", "phase": "Testing"},
    ],
    "product listing": [
        {"task": "Design product card + listing layout", "assignee": "🎨 Designer", "size": "M", "phase": "Design"},
        {"task": "Implement product listing page + grid/list view", "assignee": "⚛️ Frontend Dev", "size": "L", "phase": "Frontend"},
        {"task": "Implement filter & sort UI", "assignee": "⚛️ Frontend Dev", "size": "M", "phase": "Frontend"},
        {"task": "API: GET /products with pagination, filter, sort", "assignee": "⚙️ Backend Dev", "size": "M", "phase": "Backend"},
        {"task": "DB: Create products, categories tables", "assignee": "🏗️ Architect", "size": "M", "phase": "Setup"},
        {"task": "Seed demo products data", "assignee": "⚙️ Backend Dev", "size": "S", "phase": "Backend"},
        {"task": "Test product listing + filters", "assignee": "🧪 Tester", "size": "M", "phase": "Testing"},
    ],
    "product detail": [
        {"task": "Design product detail page + image gallery", "assignee": "🎨 Designer", "size": "M", "phase": "Design"},
        {"task": "Implement product detail page", "assignee": "⚛️ Frontend Dev", "size": "M", "phase": "Frontend"},
        {"task": "Implement image gallery/zoom component", "assignee": "⚛️ Frontend Dev", "size": "M", "phase": "Frontend"},
        {"task": "API: GET /products/:id", "assignee": "⚙️ Backend Dev", "size": "S", "phase": "Backend"},
        {"task": "Test product detail page", "assignee": "🧪 Tester", "size": "S", "phase": "Testing"},
    ],
    "cart": [
        {"task": "Design cart page + mini cart", "assignee": "🎨 Designer", "size": "M", "phase": "Design"},
        {"task": "Implement cart page (add, remove, update qty)", "assignee": "⚛️ Frontend Dev", "size": "L", "phase": "Frontend"},
        {"task": "Cart state management (local + sync with API)", "assignee": "⚛️ Frontend Dev", "size": "M", "phase": "Frontend"},
        {"task": "API: Cart CRUD endpoints", "assignee": "⚙️ Backend Dev", "size": "M", "phase": "Backend"},
        {"task": "DB: Create cart_items table", "assignee": "🏗️ Architect", "size": "S", "phase": "Setup"},
        {"task": "Test cart functionality", "assignee": "🧪 Tester", "size": "M", "phase": "Testing"},
    ],
    "checkout": [
        {"task": "Design checkout page (multi-step form)", "assignee": "🎨 Designer", "size": "L", "phase": "Design"},
        {"task": "Implement checkout flow UI", "assignee": "⚛️ Frontend Dev", "size": "L", "phase": "Frontend"},
        {"task": "Integrate payment method (VietQR/Stripe)", "assignee": "⚙️ Backend Dev", "size": "L", "phase": "Backend"},
        {"task": "API: POST /orders + order processing", "assignee": "⚙️ Backend Dev", "size": "L", "phase": "Backend"},
        {"task": "DB: Create orders, order_items tables", "assignee": "🏗️ Architect", "size": "M", "phase": "Setup"},
        {"task": "Order confirmation email", "assignee": "⚙️ Backend Dev", "size": "M", "phase": "Backend"},
        {"task": "E2E test checkout flow", "assignee": "🧪 Tester", "size": "L", "phase": "Testing"},
    ],
    "admin": [
        {"task": "Design admin dashboard layout", "assignee": "🎨 Designer", "size": "L", "phase": "Design"},
        {"task": "Implement admin product management (CRUD)", "assignee": "⚛️ Frontend Dev", "size": "L", "phase": "Frontend"},
        {"task": "Implement admin order management", "assignee": "⚛️ Frontend Dev", "size": "M", "phase": "Frontend"},
        {"task": "API: Admin endpoints (CRUD products, manage orders)", "assignee": "⚙️ Backend Dev", "size": "L", "phase": "Backend"},
        {"task": "RBAC: Admin role authorization", "assignee": "⚙️ Backend Dev", "size": "M", "phase": "Backend"},
        {"task": "Test admin functionality", "assignee": "🧪 Tester", "size": "M", "phase": "Testing"},
    ],
    "search": [
        {"task": "Design search UI (search bar + results page)", "assignee": "🎨 Designer", "size": "S", "phase": "Design"},
        {"task": "Implement search component + auto-suggest", "assignee": "⚛️ Frontend Dev", "size": "M", "phase": "Frontend"},
        {"task": "API: GET /search with full-text search", "assignee": "⚙️ Backend Dev", "size": "M", "phase": "Backend"},
        {"task": "Test search functionality", "assignee": "🧪 Tester", "size": "S", "phase": "Testing"},
    ],
    "dashboard": [
        {"task": "Design dashboard layout + widgets", "assignee": "🎨 Designer", "size": "L", "phase": "Design"},
        {"task": "Implement dashboard with charts/stats", "assignee": "⚛️ Frontend Dev", "size": "L", "phase": "Frontend"},
        {"task": "API: Dashboard analytics endpoints", "assignee": "⚙️ Backend Dev", "size": "M", "phase": "Backend"},
        {"task": "Test dashboard data accuracy", "assignee": "🧪 Tester", "size": "M", "phase": "Testing"},
    ],
    "profile": [
        {"task": "Design profile/settings page", "assignee": "🎨 Designer", "size": "S", "phase": "Design"},
        {"task": "Implement profile page + edit form", "assignee": "⚛️ Frontend Dev", "size": "S", "phase": "Frontend"},
        {"task": "API: GET/PUT /profile", "assignee": "⚙️ Backend Dev", "size": "S", "phase": "Backend"},
        {"task": "Test profile update", "assignee": "🧪 Tester", "size": "S", "phase": "Testing"},
    ],
}

# Common setup tasks added to every project
COMMON_TASKS = {
    "Setup": [
        {"task": "Design System Architecture", "assignee": "🏗️ Architect", "size": "L"},
        {"task": "Design Database Schema (ERD)", "assignee": "🏗️ Architect", "size": "L"},
        {"task": "Design API Contract", "assignee": "🏗️ Architect", "size": "M"},
        {"task": "Create Design System (colors, typography, spacing)", "assignee": "🎨 Designer", "size": "L"},
        {"task": "Setup base components (Button, Input, Card, Modal)", "assignee": "🎨 Designer", "size": "L"},
    ],
    "QA & Launch": [
        {"task": "Security audit (OWASP, dependency scan)", "assignee": "🔒 Security", "size": "M"},
        {"task": "SEO optimization (meta tags, sitemap, structured data)", "assignee": "🌐 SEO", "size": "M"},
        {"task": "Performance audit (Lighthouse, bundle analysis)", "assignee": "🌐 SEO", "size": "M"},
        {"task": "Setup CI/CD pipeline (GitHub Actions)", "assignee": "🚀 DevOps", "size": "M"},
        {"task": "Deploy to production", "assignee": "🚀 DevOps", "size": "M"},
        {"task": "Write README + API documentation", "assignee": "📚 Writer", "size": "M"},
        {"task": "Create release v1.0.0", "assignee": "🚀 DevOps", "size": "S"},
    ]
}

SIZE_EFFORT = {"S": 1, "M": 2, "L": 4, "XL": 8}


def parse_args():
    parser = argparse.ArgumentParser(description="Task Estimator")
    parser.add_argument("--features", type=str, required=True, help="List of features, comma-separated")
    parser.add_argument("--stack", type=str, default="nextjs-supabase", help="Tech stack ID")
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    return parser.parse_args()


def find_matching_tasks(feature_query):
    """Find tasks matching the feature query."""
    query = feature_query.lower().strip()

    # Direct match
    if query in TASK_TEMPLATES:
        return TASK_TEMPLATES[query]

    # Partial match
    for key, tasks in TASK_TEMPLATES.items():
        if key in query or query in key:
            return tasks

    # No match — generate generic
    return [
        {"task": f"Design {feature_query} UI", "assignee": "🎨 Designer", "size": "M", "phase": "Design"},
        {"task": f"Implement {feature_query} frontend", "assignee": "⚛️ Frontend Dev", "size": "M", "phase": "Frontend"},
        {"task": f"Implement {feature_query} backend/API", "assignee": "⚙️ Backend Dev", "size": "M", "phase": "Backend"},
        {"task": f"Test {feature_query}", "assignee": "🧪 Tester", "size": "M", "phase": "Testing"},
    ]


def estimate(features):
    """Generate task breakdown from features."""
    all_tasks = []
    task_id = 1

    # Add common setup tasks
    for task in COMMON_TASKS["Setup"]:
        all_tasks.append({
            "id": f"T-{task_id:03d}",
            "task": task["task"],
            "assignee": task["assignee"],
            "size": task["size"],
            "effort": SIZE_EFFORT[task["size"]],
            "phase": "Setup"
        })
        task_id += 1

    # Add feature-specific tasks
    for feature in features:
        feature_tasks = find_matching_tasks(feature)
        for task in feature_tasks:
            all_tasks.append({
                "id": f"T-{task_id:03d}",
                "task": task["task"],
                "assignee": task["assignee"],
                "size": task["size"],
                "effort": SIZE_EFFORT[task["size"]],
                "phase": task.get("phase", "Development"),
                "feature": feature.strip().title()
            })
            task_id += 1

    # Add common QA & Launch tasks
    for task in COMMON_TASKS["QA & Launch"]:
        all_tasks.append({
            "id": f"T-{task_id:03d}",
            "task": task["task"],
            "assignee": task["assignee"],
            "size": task["size"],
            "effort": SIZE_EFFORT[task["size"]],
            "phase": "QA & Launch"
        })
        task_id += 1

    # Calculate summary
    total_effort = sum(t["effort"] for t in all_tasks)
    by_assignee = {}
    by_phase = {}
    by_size = {"S": 0, "M": 0, "L": 0, "XL": 0}

    for t in all_tasks:
        a = t["assignee"]
        p = t["phase"]
        by_assignee[a] = by_assignee.get(a, 0) + 1
        by_phase[p] = by_phase.get(p, 0) + 1
        by_size[t["size"]] = by_size.get(t["size"], 0) + 1

    return {
        "tasks": all_tasks,
        "summary": {
            "total_tasks": len(all_tasks),
            "total_effort_points": total_effort,
            "by_size": by_size,
            "by_assignee": by_assignee,
            "by_phase": by_phase
        }
    }


def print_readable(result):
    """Print task breakdown in a readable format."""
    print("=" * 70)
    print("📋 TASK BREAKDOWN")
    print("=" * 70)

    current_phase = ""
    for t in result["tasks"]:
        if t["phase"] != current_phase:
            current_phase = t["phase"]
            print(f"\n{'━' * 70}")
            print(f"  📌 Phase: {current_phase}")
            print(f"{'━' * 70}")
            print(f"  {'ID':<8} {'Task':<40} {'Assignee':<18} {'Size':<4}")
            print(f"  {'─'*8} {'─'*40} {'─'*18} {'─'*4}")

        task_name = t["task"][:38] + ".." if len(t["task"]) > 40 else t["task"]
        print(f"  {t['id']:<8} {task_name:<40} {t['assignee']:<18} {t['size']:<4}")

    # Summary
    s = result["summary"]
    print(f"\n{'=' * 70}")
    print("  📊 SUMMARY")
    print(f"{'=' * 70}")
    print(f"  Total tasks: {s['total_tasks']}")
    print(f"  Effort points: {s['total_effort_points']}")
    print(f"  S: {s['by_size']['S']} | M: {s['by_size']['M']} | L: {s['by_size']['L']}")

    print(f"\n  👥 Assignment by Role:")
    for assignee, count in sorted(s["by_assignee"].items()):
        print(f"    {assignee}: {count} tasks")

    print(f"\n  📌 Distribution by Phase:")
    for phase, count in s["by_phase"].items():
        print(f"    {phase}: {count} tasks")

    print(f"\n{'=' * 70}")


if __name__ == "__main__":
    args = parse_args()

    features = [f.strip() for f in args.features.split(",") if f.strip()]
    result = estimate(features)

    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print_readable(result)
