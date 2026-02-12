#!/usr/bin/env python3
"""
System Strategist — Provide high-level architectural decisions and strategies.

Usage:
    python strategist.py --type tradeoff --topic "sql_vs_nosql"
    python strategist.py --type scalability --users 100000
    python strategist.py --type migration --strategy "strangler_fig"
"""

import argparse
import json
import sys
from pathlib import Path

# Path to data
DATA_FILE = Path(__file__).parent.parent / "data" / "strategy_patterns.json"

def load_data():
    if not DATA_FILE.exists():
        return {}
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def show_tradeoff(topic):
    data = load_data()
    tradeoffs = data.get("tradeoffs", {})
    
    # Partial match search
    item = None
    for key in tradeoffs:
        if topic.lower() in key.lower():
            item = tradeoffs[key]
            topic = key # Correct naming
            break
            
    if not item:
        print(f"❌ Topic '{topic}' not found in tradeoffs.")
        print(f"   Available: {', '.join(tradeoffs.keys())}")
        return

    print("\n" + "="*60)
    print(f"⚖️  TRADEOFF EVALUATION: {topic.upper().replace('_', ' ')}")
    print(f"   Context: {item['context']}")
    print("="*60)
    
    for opt in item["options"]:
        print(f"\n🔹 Option: {opt['name']}")
        print("   ✅ Pros:")
        for p in opt['pros']: print(f"      + {p}")
        print("   ⚠️ Cons:")
        for c in opt['cons']: print(f"      - {c}")
        print(f"   🎯 Best For: {opt['best_for']}")

    print("\n💡 DECISION MATRIX:")
    print(f"   {item['decision_matrix']}")
    print("="*60 + "\n")

def plan_scalability(users):
    data = load_data()
    plans = data.get("scalability_plans", {})
    
    # Determine tier
    tier = "10k_users"
    if users >= 1000000: tier = "1m_users"
    elif users >= 100000: tier = "100k_users"
    
    plan = plans.get(tier)
    
    print("\n" + "="*60)
    print(f"📈 SCALABILITY PLAN FOR {users:,} USERS")
    print(f"   Focus: {plan['focus']}")
    print("="*60)
    
    print("\n🚀 Recommended Strategies:")
    for idx, strategy in enumerate(plan['strategies'], 1):
        print(f"   {idx}. {strategy}")
        
    print("\n" + "="*60 + "\n")

def plan_migration(strategy_name):
    data = load_data()
    migrations = data.get("migration_strategies", {})
    
    # Partial match
    item = None
    for key in migrations:
        if strategy_name.lower() in key.lower():
            item = migrations[key]
            break
            
    if not item:
        print(f"❌ Strategy '{strategy_name}' not found.")
        print(f"   Available: {', '.join(migrations.keys())}")
        return

    print("\n" + "="*60)
    print(f"🔄 MIGRATION STRATEGY: {item['name']}")
    print("="*60)
    print(f"\n📝 Description: {item['description']}")
    
    print("\n👣 Execution Steps:")
    for idx, step in enumerate(item['steps'], 1):
        print(f"   {idx}. {step}")
        
    print(f"\n✅ Pros: {item['pros']}")
    print(f"⚠️ Cons: {item['cons']}")
    print("="*60 + "\n")

def main():
    parser = argparse.ArgumentParser(description="System Strategist")
    parser.add_argument("--type", type=str, required=True, choices=["tradeoff", "scalability", "migration"], help="Type of advice")
    parser.add_argument("--topic", type=str, help="Topic for tradeoff (e.g. sql_vs_nosql)")
    parser.add_argument("--users", type=int, help="Number of users for scalability planning")
    parser.add_argument("--strategy", type=str, help="Name of migration strategy")
    
    args = parser.parse_args()
    
    if args.type == "tradeoff":
        if not args.topic:
            print("Error: --topic required for tradeoff")
        else:
            show_tradeoff(args.topic)
    elif args.type == "scalability":
        if not args.users:
            print("Error: --users required for scalability")
        else:
            plan_scalability(args.users)
    elif args.type == "migration":
        if not args.strategy:
            print("Error: --strategy required for migration")
        else:
            plan_migration(args.strategy)

if __name__ == "__main__":
    main()
