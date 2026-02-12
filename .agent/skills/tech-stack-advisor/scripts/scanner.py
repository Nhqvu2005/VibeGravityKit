#!/usr/bin/env python3
"""
Tech Stack Scanner — Analyze existing codebase to detect stack.

Usage:
    python scanner.py --path "."
"""

import argparse
import os
import json
from pathlib import Path
from collections import Counter

IGNORED_DIRS = {
    "node_modules", ".git", "__pycache__", "dist", "build", "venv", "env", ".idea", ".vscode", "target", "vendor"
}

STACK_INDICATORS = {
    "package.json": "Node.js / JS Ecosystem",
    "requirements.txt": "Python",
    "pyproject.toml": "Python (Poetry/Modern)",
    "pom.xml": "Java (Maven)",
    "build.gradle": "Java/Android (Gradle)",
    "composer.json": "PHP (Composer)",
    "go.mod": "Go",
    "Cargo.toml": "Rust",
    "Gemfile": "Ruby",
    "mix.exs": "Elixir",
    "Dockerfile": "Dockerized",
    "docker-compose.yml": "Docker Compose",
    "next.config.js": "Next.js",
    "nuxt.config.js": "Nuxt.js",
    "vite.config.js": "Vite",
    "tsconfig.json": "TypeScript"
}

def scan_codebase(root_path):
    root_path = Path(root_path)
    extension_counts = Counter()
    config_files = []
    
    print(f"🔍 Scanning tech stack at: {root_path}")
    
    for root, dirs, files in os.walk(root_path):
        dirs[:] = [d for d in dirs if d not in IGNORED_DIRS]
        
        for file in files:
            if file in STACK_INDICATORS:
                config_files.append(f"{file} ({STACK_INDICATORS[file]})")
                
            ext = Path(file).suffix.lower()
            if ext:
                extension_counts[ext] += 1
                
    print("\n" + "="*50)
    print("📊 TECH STACK REPORT")
    print("="*50)
    
    print("\n🛠️  Configuration Files Detected:")
    if config_files:
        for cf in set(config_files): # Deduplicate
            print(f"   - {cf}")
    else:
        print("   (None)")
        
    print("\n📁 File Extensions Distribution:")
    total_files = sum(extension_counts.values())
    if total_files > 0:
        for ext, count in extension_counts.most_common(5):
            percent = (count / total_files) * 100
            print(f"   {ext}: {count} files ({percent:.1f}%)")
    else:
        print("   (No files found)")

    # Inference
    print("\n🧠 Inference:")
    stack = []
    if "package.json" in [f.split()[0] for f in config_files]:
        if "next.config.js" in [f.split()[0] for f in config_files]:
            stack.append("Next.js Fullstack")
        else:
            stack.append("Node.js / Web")
            
    if ".py" in extension_counts:
        stack.append("Python")
        
    if not stack:
        stack.append("Generic / Unknown")
        
    print(f"   Likely Stack: {', '.join(stack)}")
    print("="*50 + "\n")

def main():
    parser = argparse.ArgumentParser(description="Tech Stack Scanner")
    parser.add_argument("--path", type=str, default=".", help="Path to scan")
    
    args = parser.parse_args()
    scan_codebase(args.path)

if __name__ == "__main__":
    main()
