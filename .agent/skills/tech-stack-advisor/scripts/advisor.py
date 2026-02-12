#!/usr/bin/env python3
"""
Tech Stack Advisor — Compare and Recommend Technologies.

Usage:
    python advisor.py --category web --keywords "seo,fast"
    python advisor.py --compare --category frontend
"""

import argparse
import json
from pathlib import Path

DATA_FILE = Path(__file__).parent.parent / "data" / "tech_data.json"

def load_data():
    if not DATA_FILE.exists():
        return {}
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def recommend(category, keywords):
    data = load_data()
    # Simplified logic: just print relevant section
    # Enhancements: Scoring based on keywords
    print("\n" + "="*50)
    print(f"🤖 TECH RECOMMENDATION: {category.upper()}")
    print("="*50)
    
    # Map 'web' to frontend + backend for now
    categories = []
    if category == 'web':
        categories = ['frontend', 'backend', 'database']
    elif category in data['categories']:
        categories = [category]
    
    for cat in categories:
        print(f"\n📂 {cat.upper()}:")
        options = data['categories'].get(cat, {})
        
        # Simple scoring
        scored_options = []
        for key, info in options.items():
            score = 0
            text = (info['description'] + " ".join(info['pros']) + " ".join(info['use_cases'])).lower()
            
            for k in keywords.lower().split(','):
                if k.strip() in text:
                    score += 1
            
            scored_options.append((score, info))
            
        # Sort by score
        scored_options.sort(key=lambda x: x[0], reverse=True)
        
        # Print top 2
        for score, info in scored_options[:2]:
            print(f"   🔹 {info['name']} (Score: {score})")
            print(f"      Use for: {', '.join(info['use_cases'][:2])}")

    print("="*50 + "\n")

def compare(category):
    data = load_data()
    print("\n" + "="*50)
    print(f"⚖️  TECH COMPARISON: {category.upper()}")
    print("="*50)
    
    options = data['categories'].get(category, {})
    
    for key, info in options.items():
        print(f"\n🔹 {info['name']}")
        print(f"   ✅ Pros: {', '.join(info['pros'])}")
        print(f"   ❌ Cons: {', '.join(info['cons'])}")
        print(f"   💡 Best for: {', '.join(info['use_cases'])}")
        
    print("="*50 + "\n")

def main():
    parser = argparse.ArgumentParser(description="Tech Stack Advisor")
    parser.add_argument("--category", type=str, required=True, help="web, frontend, backend, database")
    parser.add_argument("--keywords", type=str, default="", help="comma separated keywords")
    parser.add_argument("--compare", action="store_true", help="Show comparison view")
    
    args = parser.parse_args()
    
    if args.compare:
        compare(args.category)
    else:
        recommend(args.category, args.keywords)

if __name__ == "__main__":
    main()
