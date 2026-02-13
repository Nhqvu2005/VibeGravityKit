#!/usr/bin/env python3
"""
Project Management Assistant — Project estimation, risk analysis, and timeline planning.

Usage:
    python pm_assistant.py --action scope --features "login,cart,checkout,admin,blog,analytics,ai-chat"
    python pm_assistant.py --action risk --keywords "ai,payment"
    python pm_assistant.py --action plan --weeks 8
"""

import argparse
import json
import sys
import os
from pathlib import Path

# Path to data
DATA_FILE = Path(__file__).parent.parent / "data" / "pm_data.json"

def load_data():
    if not DATA_FILE.exists():
        return {}
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def check_scope(features_str, timeline_weeks=4):
    """Analyze scope vs timeline."""
    data = load_data()
    features = [f.strip() for f in features_str.split(",") if f.strip()]
    count = len(features)
    
    limits = data.get("scope_limits", {})
    mode = "mvp" if timeline_weeks <= 4 else "v1"
    limit = limits.get(mode, {})
    
    print("\n" + "="*60)
    print(f"🧐 SCOPE ANALYSIS (Mode: {mode.upper()})")
    print("="*60)
    print(f"  • Input Features: {count}")
    print(f"  • Max Recommended: {limit.get('max_features', 0)}")
    
    if count > limit.get("max_features", 0):
        print(f"\n  ⚠️  WARNING: Scope is too big for {mode.upper()}!")
        print(f"      {limit.get('description')}")
        print(f"  👉 Suggestion: Cut {count - limit.get('max_features')} features directly.")
    else:
        print("\n  ✅ Scope looks good! Manageable.")
        
    print("="*60 + "\n")

def assess_risk(keywords_str):
    """Identify project risks."""
    data = load_data()
    keywords = [k.strip().lower() for k in keywords_str.split(",")]
    risks = data.get("risks", {}).get("tech", [])
    
    found_risks = []
    
    for r in risks:
        if any(k in r["keyword"] for k in keywords):
            found_risks.append(r)
            
    print("\n" + "="*60)
    print("🛡️  RISK ASSESSMENT")
    print("="*60)
    
    if not found_risks:
        print("  ✅ No high-risk tech factors identified based on keywords.")
    else:
        for r in found_risks:
            print(f"\n  🔴 Risk: {r['risk']}")
            print(f"     Key: {r['keyword']}")
            print(f"     🛡️ Mitigation: {r['mitigation']}")
            
    print("\n" + "="*60 + "\n")

def create_milestone_plan(weeks):
    """Generate milestone breakdown."""
    data = load_data()
    template = data.get("milestone_templates", {}).get("standard", [])
    
    print("\n" + "="*60)
    print(f"📅 MILESTONE PLAN ({weeks} weeks)")
    print("="*60)
    
    total_weeks = float(weeks)
    current_week = 0.0
    
    for phase in template:
        duration = phase["duration_ratio"] * total_weeks
        start = current_week
        end = current_week + duration
        current_week = end
        
        # Format weeks nicely
        range_str = f"Week {start:.1f} - {end:.1f}"
        if start == 0: range_str = f"Start - Week {end:.1f}"
        
        print(f"\n  📍 {phase['phase']}")
        print(f"     🕒 Duration: {duration:.1f} weeks ({range_str})")
        print(f"     🎯 Focus: {phase['focus']}")
        
    print("\n" + "="*60 + "\n")

def main():
    parser = argparse.ArgumentParser(description="Project Management Assistant")
    parser.add_argument("--action", type=str, required=True, choices=["scope", "risk", "plan"], help="Action to perform")
    parser.add_argument("--features", type=str, default="", help="Comma-separated features list")
    parser.add_argument("--keywords", type=str, default="", help="Keywords for risk check (e.g. ai, payment)")
    parser.add_argument("--weeks", type=float, default=4, help="Project timeline in weeks")
    
    args = parser.parse_args()
    
    if args.action == "scope":
        check_scope(args.features, args.weeks)
    elif args.action == "risk":
        assess_risk(args.keywords)
    elif args.action == "plan":
        create_milestone_plan(args.weeks)

if __name__ == "__main__":
    main()
