#!/usr/bin/env python3
"""
Strategic Planning Advisor — System strategy and long-term architecture advice.

Usage:
    python strategy.py --phase "mvp" --domain "ecommerce"
"""

import argparse
import json
import sys
import os
from pathlib import Path

# Path to the data file
DATA_FILE = Path(__file__).parent.parent / "data" / "strategies.json"

def load_data():
    """Load strategy data."""
    if not DATA_FILE.exists():
        print(f"Error: Database file not found at {DATA_FILE}")
        sys.exit(1)
    
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def get_advice(phase, domain):
    """Retrieve advice based on project phase and domain."""
    data = load_data()
    advice = {
        "phase": None,
        "domain": None
    }

    # Find phase advice
    for item in data:
        if "phase" in item and (phase.lower() in item["id"] or phase.lower() in item["phase"].lower()):
            advice["phase"] = item
            break
    
    # Default to MVP if not found
    if not advice["phase"] and phase:
        for item in data:
            if item["id"] == "scale-mvp":
                advice["phase"] = item
                break

    # Find domain advice
    for item in data:
        if "domain" in item and (domain.lower() in item["id"] or domain.lower() in item["domain"].lower()):
            advice["domain"] = item
            break
            
    return advice

def print_strategy(advice):
    """Print strategic advice in a readable format."""
    print("\n" + "="*80)
    print("🧠 STRATEGIC PLANNING ADVISOR")
    print("="*80)

    # Phase Advice
    if advice["phase"]:
        p = advice["phase"]
        print(f"\n📌 PHASE: {p['phase']}")
        print(f"   Architecture: {p['architecture']}")
        print(f"   Infrastructure: {p['infrastructure']}")
        
        print("\n   ✅ Best Practices:")
        for bp in p['best_practices']:
            print(f"      • {bp}")
            
        print("\n   ⚠️ Anti-Patterns (Avoid):")
        for ap in p['anti_patterns']:
            print(f"      ✕ {ap}")
            
        print(f"\n   🔧 Maintenance Focus: {p['maintenance_focus']}")

    # Domain Advice
    if advice["domain"]:
        d = advice["domain"]
        print(f"\n" + "-"*80)
        print(f"🏭 DOMAIN SPECIFIC: {d['domain']}")
        
        print("\n   🛡️ Critical Considerations:")
        for cc in d['critical_considerations']:
            print(f"      ! {cc}")
            
        print(f"\n   💣 Tech Debt Warning: {d['tech_debt_warning']}")

    print("\n" + "="*80 + "\n")

def main():
    parser = argparse.ArgumentParser(description="Strategic Planning Advisor")
    parser.add_argument("--phase", type=str, default="mvp", help="Project phase: mvp, growth, scale")
    parser.add_argument("--domain", type=str, default="general", help="Domain: ecommerce, saas, collaborative...")
    parser.add_argument("--json", action="store_true", help="Output JSON")
    
    args = parser.parse_args()
    
    result = get_advice(args.phase, args.domain)
    
    if args.json:
        print(json.dumps(result, indent=2))
    else:
        print_strategy(result)

if __name__ == "__main__":
    main()
