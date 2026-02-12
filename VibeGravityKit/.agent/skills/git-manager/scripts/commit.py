#!/usr/bin/env python3
"""
Git Manager — Standardized Semantic Commits.

Usage:
    python commit.py --type feat --scope auth --msg "Add login endpoint"
    python commit.py --interactive
"""

import argparse
import subprocess
import sys

TYPES = [
    "feat", "fix", "docs", "style", "refactor", "perf", "test", "build", "ci", "chore", "revert"
]

def run_git_commit(commit_type, scope, message):
    scope_part = f"({scope})" if scope else ""
    full_message = f"{commit_type}{scope_part}: {message}"
    
    cmd = ["git", "commit", "-m", full_message]
    print(f"🚀 Executing: {' '.join(cmd)}")
    try:
        subprocess.run(cmd, check=True)
        print("✅ Commit successful!")
    except subprocess.CalledProcessError as e:
        print(f"❌ Error committing: {e}")
        sys.exit(1)

def interactive():
    print("📝 Interactive Commit")
    print("Choose type:")
    for i, t in enumerate(TYPES, 1):
        print(f"  {i}. {t}")
    
    type_idx = input("Type number (default 1): ")
    try:
        commit_type = TYPES[int(type_idx)-1]
    except:
        commit_type = "feat"
        
    scope = input("Scope (optional): ")
    message = input("Message: ")
    
    if not message:
        print("Error: Message required")
        sys.exit(1)
        
    run_git_commit(commit_type, scope, message)

def main():
    parser = argparse.ArgumentParser(description="Semantic Commit Helper")
    parser.add_argument("--type", choices=TYPES)
    parser.add_argument("--scope")
    parser.add_argument("--msg")
    parser.add_argument("--interactive", "-i", action="store_true")
    
    args = parser.parse_args()
    
    if args.interactive:
        interactive()
    elif args.type and args.msg:
        run_git_commit(args.type, args.scope, args.msg)
    else:
        # Default to interactive if no args
        interactive()

if __name__ == "__main__":
    main()
