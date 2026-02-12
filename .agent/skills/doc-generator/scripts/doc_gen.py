#!/usr/bin/env python3
"""
Doc Generator — Setup MkDocs / Sphinx.

Usage:
    python doc_gen.py --type mkdocs --name "My Docs"
"""

import argparse
import os

MKDOCS_YML = """site_name: {name}
theme:
  name: material

nav:
  - Home: index.md
  - API: api.md
  - Architecture: architecture.md
"""

def generate_mkdocs(name):
    print(f"📚 Setting up MkDocs for {name}...")
    
    with open('mkdocs.yml', 'w', encoding='utf-8') as f:
        f.write(MKDOCS_YML.format(name=name))
    print("✅ Created mkdocs.yml")
    
    os.makedirs('docs', exist_ok=True)
    with open('docs/index.md', 'w', encoding='utf-8') as f:
        f.write(f"# {name}\n\nWelcome to the documentation.")
    print("✅ Created docs/index.md")
    
    print("\nNext Steps:")
    print("1. pip install mkdocs-material")
    print("2. mkdocs serve")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--name", default="Project Docs")
    parser.add_argument("--type", default="mkdocs")
    args = parser.parse_args()
    
    if args.type == "mkdocs":
        generate_mkdocs(args.name)

if __name__ == "__main__":
    main()
