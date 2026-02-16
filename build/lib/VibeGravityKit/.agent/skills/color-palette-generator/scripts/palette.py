#!/usr/bin/env python3
"""
Color Palette Generator — Generate harmonious color palettes.

Usage:
    python palette.py --style modern
"""

import argparse
import json
import sys
from pathlib import Path

# Path to data
DATA_FILE = Path(__file__).parent.parent / "data" / "palettes.json"

def load_data():
    if not DATA_FILE.exists():
        return {}
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def generate_palette(style):
    data = load_data()
    palette = data.get(style.lower())
    
    print("\n" + "="*50)
    print(f"🎨 COLOR PALETTE: {style.upper()}")
    print("="*50)
    
    if not palette:
        print(f"⚠️  Style '{style}' not found. Available: {', '.join(data.keys())}")
        return

    print(f"   Primary:   {palette['primary']}  ██████")
    print(f"   Secondary: {palette['secondary']}  ██████")
    print(f"   Accent:    {palette['accent']}  ██████")
    print(f"   Neutral:   {palette['neutral']}  ██████")
    print(f"   Background:{palette['background']}  ██████")
    
    print("\n   CSS Variables:")
    print("   :root {")
    for key, value in palette.items():
        print(f"     --color-{key}: {value};")
    print("   }")
    
    print("="*50 + "\n")

def main():
    parser = argparse.ArgumentParser(description="Color Palette Generator")
    parser.add_argument("--style", type=str, default="modern", help="Style: modern, corporate, playful, dark_tech, luxury")
    
    args = parser.parse_args()
    generate_palette(args.style)

if __name__ == "__main__":
    main()
