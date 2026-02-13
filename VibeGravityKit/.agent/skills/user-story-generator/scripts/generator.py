#!/usr/bin/env python3
"""
User Story Generator — Generate user story templates from features and roles.

Usage:
    python generator.py --features "login,product listing,cart,checkout" --roles "buyer,admin"
"""

import argparse
import json
import sys

# === User Story Templates by feature type ===
STORY_TEMPLATES = {
    "login": {
        "title": "Login",
        "stories": [
            {
                "role": "user",
                "action": "log in with email and password",
                "benefit": "access my account and use personal features",
                "priority": "Must",
                "size": "M",
                "criteria": [
                    "Given login page, when correct email + password entered, then redirect to dashboard/home",
                    "Given login page, when wrong password entered 3 times, then show error and retry after 30s",
                    "Given not logged in, when accessing protected page, then redirect to login page",
                    "Given logged in successfully, when reloading page, then session persists"
                ]
            },
            {
                "role": "user",
                "action": "log in with Google/Facebook",
                "benefit": "log in quickly without remembering passwords",
                "priority": "Should",
                "size": "M",
                "criteria": [
                    "Given login page, when clicking 'Log in with Google', then redirect to Google OAuth",
                    "Given OAuth successful, when callback received, then create/update account and log in"
                ]
            }
        ]
    },
    "register": {
        "title": "Account Registration",
        "stories": [
            {
                "role": "user",
                "action": "register a new account with email",
                "benefit": "start using the service",
                "priority": "Must",
                "size": "M",
                "criteria": [
                    "Given registration page, when valid info entered, then account created successfully",
                    "Given email already exists, when registering, then show error 'Email already in use'",
                    "Given weak password, when submitting, then require stronger password",
                    "Given registration successful, when finished, then send confirmation email"
                ]
            }
        ]
    },
    "product listing": {
        "title": "Product Listing",
        "stories": [
            {
                "role": "buyer",
                "action": "view product list by category",
                "benefit": "find products I am interested in",
                "priority": "Must",
                "size": "L",
                "criteria": [
                    "Given category page, when page loads, then display products in grid/list",
                    "Given many products, when scrolling, then load more (infinite scroll or pagination)",
                    "Given each product, when displayed, then show image, name, price, rating"
                ]
            },
            {
                "role": "buyer",
                "action": "filter products by price, color, size",
                "benefit": "quickly find the right product",
                "priority": "Should",
                "size": "M",
                "criteria": [
                    "Given category page, when price filter selected, then only show products in range",
                    "Given multiple filters, when selected together, then apply AND logic",
                    "Given active filter, when removed, then reset list"
                ]
            },
            {
                "role": "buyer",
                "action": "search for products by keyword",
                "benefit": "find products by name quickly",
                "priority": "Must",
                "size": "M",
                "criteria": [
                    "Given search bar, when keyword entered, then show relevant results",
                    "Given keyword mismatch, when searching, then show 'No products found'",
                    "Given typing, when stopped for 300ms, then auto-suggest results"
                ]
            }
        ]
    },
    "product detail": {
        "title": "Product Detail",
        "stories": [
            {
                "role": "buyer",
                "action": "view product details with image, price, description",
                "benefit": "evaluate product before buying",
                "priority": "Must",
                "size": "M",
                "criteria": [
                    "Given detail page, when loaded, then show gallery, price, full description",
                    "Given product variants, when size/color selected, then update price and stock",
                    "Given product image, when clicked, then zoom/lightbox"
                ]
            }
        ]
    },
    "cart": {
        "title": "Shopping Cart",
        "stories": [
            {
                "role": "buyer",
                "action": "add product to cart",
                "benefit": "save items to purchase later",
                "priority": "Must",
                "size": "M",
                "criteria": [
                    "Given product detail page, when clicking 'Add to Cart', then product added to cart",
                    "Given product already in cart, when added again, then increase quantity",
                    "Given add successful, when animating, then show badge count on cart icon"
                ]
            },
            {
                "role": "buyer",
                "action": "view and edit shopping cart",
                "benefit": "review before checkout",
                "priority": "Must",
                "size": "M",
                "criteria": [
                    "Given cart page, when loaded, then show list of products with image, name, price, qty",
                    "Given item in cart, when quantity changed, then update total price",
                    "Given item in cart, when delete clicked, then remove from cart",
                    "Given empty cart, when loaded, then show 'Cart is empty' + link to shop"
                ]
            }
        ]
    },
    "checkout": {
        "title": "Checkout",
        "stories": [
            {
                "role": "buyer",
                "action": "checkout order",
                "benefit": "complete purchase",
                "priority": "Must",
                "size": "L",
                "criteria": [
                    "Given checkout page, when loaded, then show shipping address form",
                    "Given valid form, when payment method selected, then show payment details",
                    "Given payment successful, when completed, then show confirmation page + send email",
                    "Given payment failed, when error, then show error message + allow retry"
                ]
            }
        ]
    },
    "admin": {
        "title": "Administration",
        "stories": [
            {
                "role": "admin",
                "action": "manage products (add, edit, delete)",
                "benefit": "update product catalog",
                "priority": "Must",
                "size": "L",
                "criteria": [
                    "Given admin panel, when adding new product, then product appears on website",
                    "Given product list, when editing info, then update immediately",
                    "Given product, when deleting, then confirm before permanent deletion"
                ]
            },
            {
                "role": "admin",
                "action": "view and manage orders",
                "benefit": "process orders timely",
                "priority": "Must",
                "size": "M",
                "criteria": [
                    "Given admin panel, when viewing orders, then list with status filter",
                    "Given new order, when status updated, then notify buyer"
                ]
            }
        ]
    },
    "dashboard": {
        "title": "Dashboard",
        "stories": [
            {
                "role": "user",
                "action": "view dashboard with overview stats",
                "benefit": "quickly grasp status",
                "priority": "Must",
                "size": "L",
                "criteria": [
                    "Given dashboard, when loaded, then show stats cards (users, revenue, orders...)",
                    "Given charts, when hovering, then show detailed tooltip",
                    "Given data changes, when refreshing, then update realtime"
                ]
            }
        ]
    },
    "profile": {
        "title": "User Profile",
        "stories": [
            {
                "role": "user",
                "action": "view and edit personal info",
                "benefit": "keep account details up to date",
                "priority": "Should",
                "size": "S",
                "criteria": [
                    "Given profile page, when loaded, then show current info",
                    "Given edit form, when submitted, then update and show success message",
                    "Given avatar upload, when image selected, then resize and save"
                ]
            }
        ]
    }
}


def parse_args():
    parser = argparse.ArgumentParser(description="User Story Generator")
    parser.add_argument("--features", type=str, required=True, help="List of features, comma-separated")
    parser.add_argument("--roles", type=str, default="user", help="List of roles, comma-separated")
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    return parser.parse_args()


def find_matching_template(feature_query):
    """Find the best matching template for a feature query."""
    query_lower = feature_query.lower().strip()

    # Direct match
    if query_lower in STORY_TEMPLATES:
        return STORY_TEMPLATES[query_lower]

    # Partial match
    for key, template in STORY_TEMPLATES.items():
        if key in query_lower or query_lower in key:
            return template
        if template["title"].lower() in query_lower or query_lower in template["title"].lower():
            return template

    return None


def generate_stories(features, roles):
    """Generate user stories from features."""
    all_stories = []
    story_id = 1

    for feature in features:
        template = find_matching_template(feature)

        if template:
            for story in template["stories"]:
                # Replace role if needed
                role = story["role"]
                if role == "user" and roles and roles[0] != "user":
                    role = roles[0]

                all_stories.append({
                    "id": f"US-{story_id:03d}",
                    "feature": template["title"],
                    "role": role,
                    "action": story["action"],
                    "benefit": story["benefit"],
                    "priority": story["priority"],
                    "size": story["size"],
                    "criteria": story["criteria"]
                })
                story_id += 1
        else:
            # Generate generic story for unknown features
            all_stories.append({
                "id": f"US-{story_id:03d}",
                "feature": feature.strip().title(),
                "role": roles[0] if roles else "user",
                "action": f"use the {feature.strip()} feature",
                "benefit": "meet my needs",
                "priority": "Should",
                "size": "M",
                "criteria": [
                    f"Given {feature.strip()} page, when loaded, then display full content",
                    f"Given {feature.strip()}, when interacting, then respond as expected"
                ]
            })
            story_id += 1

    return all_stories


def print_readable(stories):
    """Print user stories in a readable format."""
    priority_emoji = {"Must": "🔴", "Should": "🟡", "Could": "🟢", "Won't": "⚪"}

    print("=" * 60)
    print("📝 USER STORIES")
    print("=" * 60)

    current_feature = ""
    for story in stories:
        if story["feature"] != current_feature:
            current_feature = story["feature"]
            print(f"\n{'━' * 60}")
            print(f"  📌 {current_feature}")
            print(f"{'━' * 60}")

        emoji = priority_emoji.get(story["priority"], "⚪")
        print(f"\n  {story['id']}: {story['action']}")
        print(f"  Priority: {emoji} {story['priority']} | Size: {story['size']}")
        print(f"  As a {story['role']}, I want to {story['action']},")
        print(f"  so that {story['benefit']}.")
        print(f"  Acceptance Criteria:")
        for ac in story["criteria"]:
            print(f"    ☐ {ac}")

    # Summary
    total = len(stories)
    by_priority = {}
    for s in stories:
        by_priority[s["priority"]] = by_priority.get(s["priority"], 0) + 1

    print(f"\n{'=' * 60}")
    print(f"  📊 Total: {total} stories")
    for p, count in sorted(by_priority.items()):
        emoji = priority_emoji.get(p, "⚪")
        print(f"    {emoji} {p}: {count}")
    print(f"{'=' * 60}")


if __name__ == "__main__":
    args = parse_args()

    features = [f.strip() for f in args.features.split(",") if f.strip()]
    roles = [r.strip() for r in args.roles.split(",") if r.strip()]

    stories = generate_stories(features, roles)

    if args.json:
        print(json.dumps(stories, ensure_ascii=False, indent=2))
    else:
        print_readable(stories)
