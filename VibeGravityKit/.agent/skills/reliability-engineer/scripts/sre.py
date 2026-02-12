#!/usr/bin/env python3
"""
Reliability Engineer — Observability, Incident Analysis, and Performance Tuning.

Usage:
    python sre.py --action observability
    python sre.py --action incident --title "Database Outage"
    python sre.py --action performance --area database
"""

import argparse
import json
import sys
from pathlib import Path

# Path to data
DATA_FILE = Path(__file__).parent.parent / "data" / "reliability.json"

def load_data():
    if not DATA_FILE.exists():
        return {}
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def show_observability():
    data = load_data()
    obs = data.get("observability_stack", {})
    
    print("\n" + "="*60)
    print("🔭 OBSERVABILITY DESIGNS")
    print("="*60)
    
    print(f"\n📊 Metrics (Monitoring):")
    print(f"   Stack: {obs['metrics']['stack']}")
    print(f"   Keys: {', '.join(obs['metrics']['key_metrics'])}")
    
    print(f"\n📝 Logging:")
    print(f"   Stack: {obs['logging']['stack']}")
    print(f"   Best Practices: {', '.join(obs['logging']['practices'])}")

    print(f"\nSearching Tracing:")
    print(f"   Stack: {obs['tracing']['stack']}")

    print("\n" + "="*60 + "\n")

def create_incident_report(title):
    data = load_data()
    template = data.get("incident_templates", {}).get("rca", {})
    
    print("\n" + "="*60)
    print(f"🚨 INCIDENT REPORT TEMPLATE: {title}")
    print("="*60)
    
    print(f"\n# {template['title']}")
    for section in template['sections']:
        print(f"\n## {section}")
        print("   (Enter details here...)")
        
    print("\n" + "="*60 + "\n")

def suggest_performance(area):
    data = load_data()
    tips = data.get("performance_tuning", {}).get(area.lower(), [])
    
    print("\n" + "="*60)
    print(f"⚡ PERFORMANCE TUNING: {area.upper()}")
    print("="*60)
    
    if not tips:
        print(f"❌ Area '{area}' not found. Try: database, backend, frontend")
    else:
        for tip in tips:
            print(f"   🚀 {tip}")
            
    print("\n" + "="*60 + "\n")


def main():
    parser = argparse.ArgumentParser(description="Reliability Engineer (SRE)")
    parser.add_argument("--action", type=str, required=True, choices=["observability", "incident", "performance"], help="Action to perform")
    parser.add_argument("--title", type=str, default="Incident", help="Title for incident report")
    parser.add_argument("--area", type=str, default="backend", help="Area for performance tuning")
    
    args = parser.parse_args()
    
    if args.action == "observability":
        show_observability()
    elif args.action == "incident":
        create_incident_report(args.title)
    elif args.action == "performance":
        suggest_performance(args.area)

if __name__ == "__main__":
    main()
