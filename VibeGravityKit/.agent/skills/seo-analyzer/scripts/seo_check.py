#!/usr/bin/env python3
"""
SEO Analyzer — Check Meta Tags & Structure (Zero Token).

Usage:
    python seo_check.py <file_path>
"""

import argparse
import re
from pathlib import Path

CHECKS = [
    (r'<title>.*?</title>', 'Title Tag'),
    (r'<meta\s+name=["\']description["\']', 'Meta Description'),
    (r'<meta\s+property=["\']og:image["\']', 'Open Graph Image'),
    (r'<h1', 'H1 Tag'),
    (r'alt=["\'].*?["\']', 'Image Alt Text')
]

def check_file(path):
    print(f"🔍 Checking SEO for {path}...")
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
        
    score = 0
    for pattern, name in CHECKS:
        if re.search(pattern, content, re.IGNORECASE):
            print(f"✅ {name} found")
            score += 1
        else:
            print(f"❌ {name} MISSING")
            
    print(f"\nSEO Score: {score}/{len(CHECKS)}")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("file")
    args = parser.parse_args()
    check_file(args.file)

if __name__ == "__main__":
    main()
