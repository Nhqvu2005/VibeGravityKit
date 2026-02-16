#!/usr/bin/env python3
"""
Architecture Auditor — Review code and design against standards.

Usage:
    python auditor.py --check security
    python auditor.py --check performance
    python auditor.py --check naming
    python auditor.py --check debt
"""

import argparse
import json
import sys
from pathlib import Path

# Path to check data
DATA_FILE = Path(__file__).parent.parent / "data" / "standards.json"

def load_data():
    if not DATA_FILE.exists():
        return {}
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def run_check(category):
    data = load_data()
    
    print("\n" + "="*60)
    print(f"🕵️  ARCHITECTURE AUDIT: {category.upper()}")
    print("="*60)
    
    if category == "security":
        print("\n🔒 Security Checklist:")
        for item in data.get("security", {}).get("checklist", []):
            print(f"   [ ] {item}")
        print("\n🛡️ Recommended Headers:")
        for k, v in data.get("security", {}).get("headers", {}).items():
            print(f"   {k}: {v}")
            
    elif category == "performance":
        print("\n🚀 Performance Checklist:")
        for item in data.get("performance", {}).get("checklist", []):
            print(f"   [ ] {item}")
            
    elif category == "naming":
        print("\nABC Naming Conventions:")
        for k, v in data.get("naming_conventions", {}).items():
            print(f"   • {k.replace('_', ' ').title()}: {v}")
            
    elif category == "debt":
        print("\n💸 Technical Debt Indicators (Anti-patterns):")
        for item in data.get("tech_debt_indicators", []):
            print(f"   ⚠️  {item}")
            
    else:
        print(f"Unknown category: {category}")
        
    print("\n" + "="*60 + "\n")

def main():
    parser = argparse.ArgumentParser(description="Architecture Auditor")
    parser.add_argument("--check", type=str, required=True, choices=["security", "performance", "naming", "debt"], help="Audit category")
    
    args = parser.parse_args()
    run_check(args.check)

if __name__ == "__main__":
    main()
