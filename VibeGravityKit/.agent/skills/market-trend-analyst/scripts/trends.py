#!/usr/bin/env python3
"""
Market Trend Analyst — Phân tích xu hướng thị trường và kỳ vọng người dùng.

Usage:
    python trends.py --domain "ecommerce"
"""

import argparse
import json
import sys
import os
from pathlib import Path

# Path to the data file
DATA_FILE = Path(__file__).parent.parent / "data" / "trends.json"

def load_data():
    """Load trends data."""
    if not DATA_FILE.exists():
        print(f"Error: Database file not found at {DATA_FILE}")
        sys.exit(1)
    
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def analyze(domain):
    """Retrieve market trends for a domain."""
    data = load_data()
    
    # Simple search
    for item in data:
        if domain.lower() in item["domain"].lower():
            return item
            
    return None

def print_analysis(result, domain):
    """Print analysis in a readable format."""
    print("\n" + "="*80)
    print("📈 MARKET TREND ANALYST")
    print("="*80)

    if not result:
        print(f"\n⚠️  Không tìm thấy dữ liệu cho domain: '{domain}'")
        print("   Các domains hỗ trợ: ecommerce, saas, fintech, edtech, healthtech")
        print("\n" + "="*80 + "\n")
        return

    print(f"\n🏭 DOMAIN: {result['domain'].upper()}")
    print(f"📄 Overview: {result['market_summary']}")
    
    print("\n🔥 Xu Hướng Nổi Bật (Trends):")
    print("-" * 80)
    print(f"{'Trend':<35} {'Impact':<10} {'Adoption':<15}")
    print("-" * 80)
    
    for t in result["trends"]:
        print(f"{t['trend']:<35} {t['impact']:<10} {t['adoption']:<15}")
        print(f"   ↳ {t['description']}")
        print()

    print("\n👥 Kỳ Vọng Người Dùng (User Expectations):")
    for exp in result["user_expectations"]:
        print(f"   ❤️  {exp}")

    print("\n" + "="*80 + "\n")

def main():
    parser = argparse.ArgumentParser(description="Market Trend Analyst")
    parser.add_argument("--domain", type=str, required=True, help="Lĩnh vực cần phân tích: ecommerce, saas, fintech...")
    parser.add_argument("--json", action="store_true", help="Output JSON")
    
    args = parser.parse_args()
    
    result = analyze(args.domain)
    
    if args.json:
        if result:
            print(json.dumps(result, ensure_ascii=False, indent=2))
        else:
            print("{}")
    else:
        print_analysis(result, args.domain)

if __name__ == "__main__":
    main()
