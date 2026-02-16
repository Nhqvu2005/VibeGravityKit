#!/usr/bin/env python3
"""
Product Designer — UX tools for Research, Flows, Usability, and Handoff.

Usage:
    python ux_tools.py --action persona --type "mobile_shopper"
    python ux_tools.py --action flow --task "checkout"
    python ux_tools.py --action usability
    python ux_tools.py --action handoff --platform "mobile_app"
"""

import argparse
import json
import sys
from pathlib import Path

# Path to data
DATA_FILE = Path(__file__).parent.parent / "data" / "ux_data.json"

def load_data():
    if not DATA_FILE.exists():
        return {}
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def generate_persona(persona_type):
    data = load_data()
    personas = data.get("personas", {})
    
    # Partial match
    found = None
    for k, v in personas.items():
        if persona_type.lower() in k.lower():
            found = v
            break
            
    if not found:
        print(f"❌ Persona '{persona_type}' not found. Defaulting to Generic.")
        found = personas.get("generic")

    print("\n" + "="*50)
    print(f"👤 USER PERSONA: {found['name']}")
    print("="*50)
    print("🎯 GOALS:")
    for g in found['goals']: print(f"   • {g}")
    print("\n😫 PAIN POINTS:")
    for p in found['pain_points']: print(f"   • {p}")
    print("="*50 + "\n")

def generate_flow(task):
    print("\n" + "="*50)
    print(f"🌊 USER FLOW: {task.upper()}")
    print("="*50)
    print(f"1. Start: User intends to {task}")
    print("2. [Screen: Entry Point] -> User taps functionality")
    print("3. System checks condition (Login/Data)")
    print("   ↳ If Fail: Show Error/Login Screen")
    print("4. [Screen: Main Action] -> User inputs data/selects option")
    print("5. [Screen: Review/Confirm] -> User verifies")
    print("6. End: System shows Success state")
    print("="*50 + "\n")

def check_usability():
    data = load_data()
    heuristics = data.get("usability_heuristics", [])
    
    print("\n" + "="*50)
    print("🕵️ USABILITY HEURISTICS CHECKLIST")
    print("="*50)
    for idx, h in enumerate(heuristics, 1):
        print(f"[ ] {idx}. {h}")
    print("="*50 + "\n")

def check_handoff(platform):
    data = load_data()
    checklist = data.get("handoff_checklist", {}).get(platform.lower())
    constraints = data.get("tech_constraints", {}).get(platform.lower().split("_")[0], []) # simple match
    
    print("\n" + "="*50)
    print(f"📦 DEV HANDOFF CHECKLIST: {platform.upper()}")
    print("="*50)
    
    if checklist:
        print("\n✅ Deliverables Check:")
        for item in checklist:
            print(f"   [ ] {item}")
    
    if constraints:
        print("\n⚠️ Technical Constraints to Remember:")
        for c in constraints:
            print(f"   ! {c}")
            
    print("="*50 + "\n")

def main():
    parser = argparse.ArgumentParser(description="Product Designer Tools")
    parser.add_argument("--action", type=str, required=True, choices=["persona", "flow", "usability", "handoff"], help="Action")
    parser.add_argument("--type", type=str, default="generic", help="Persona type")
    parser.add_argument("--task", type=str, default="task", help="Task for flow")
    parser.add_argument("--platform", type=str, default="web", help="Platform for handoff (web, mobile_app)")
    
    args = parser.parse_args()
    
    if args.action == "persona":
        generate_persona(args.type)
    elif args.action == "flow":
        generate_flow(args.task)
    elif args.action == "usability":
        check_usability()
    elif args.action == "handoff":
        check_handoff(args.platform)

if __name__ == "__main__":
    main()
