#!/usr/bin/env python3
"""
Diff Applier — Apply SEARCH/REPLACE blocks safely.

Usage:
    python apply_patch.py <target_file> <patch_file>
"""

import argparse
import sys
import shutil
import subprocess
from pathlib import Path

def apply_patch(target_file, patch_file):
    target = Path(target_file)
    patch = Path(patch_file)
    
    if not target.exists():
        print(f"❌ Target file not found: {target}")
        sys.exit(1)
        
    if not patch.exists():
        print(f"❌ Patch file not found: {patch}")
        sys.exit(1)
        
    print(f"🔧 Applying patch to {target.name}...")
    
    with open(target, 'r', encoding='utf-8') as f:
        content = f.read()
        
    with open(patch, 'r', encoding='utf-8') as f:
        patch_content = f.read()
        
    # Parse blocks
    blocks = patch_content.split('<<<<<<< SEARCH')
    if len(blocks) < 2:
        print("❌ No SEARCH blocks found in patch.")
        sys.exit(1)
        
    new_content = content
    changes_count = 0
    
    for block in blocks[1:]: # Skip preamble
        if '=======' not in block or '>>>>>>> REPLACE' not in block:
            print("❌ Malformed block (missing separator or end tag)")
            continue
            
        search_part, rest = block.split('=======', 1)
        replace_part, _ = rest.split('>>>>>>> REPLACE', 1)
        
        search_text = search_part.strip()
        replace_text = replace_part.strip()
        
        # Try to find exact match (ignoring leading/trailing whitespace of the block itself, but keeping internal structure)
        # Actually, simpler: search for the exact lines
        
        if search_text not in new_content:
             # Try stricter normalization if exact match fails?
             # For now, strict.
             print(f"❌ Could not find SEARCH block:\n{search_text[:50]}...")
             continue
             
        # Check uniqueness
        if new_content.count(search_text) > 1:
            print(f"❌ SEARCH block matches multiple locations. Aborting block:\n{search_text[:50]}...")
            continue
            
        new_content = new_content.replace(search_text, replace_text)
        changes_count += 1
        
    if changes_count == 0:
        print("⚠️ No changes applied.")
        sys.exit(1)
        
    # Backup
    backup = target.with_suffix('.bak')
    shutil.copy2(target, backup)
    print(f"📦 Backup created: {backup.name}")
    
    # Write
    with open(target, 'w', encoding='utf-8') as f:
        f.write(new_content)
        
    print(f"✅ Applied {changes_count} changes.")
    
    # Auto-Lint
    run_linter(target)
    
    # Auto-Index
    run_indexer(target)

def run_linter(target):
    print("\n🔍 Running Linter...")
    # Simple heuristic
    if target.suffix == '.py':
        # Try flake8 or pylint
        try:
            subprocess.run(["flake8", str(target)], check=False)
        except FileNotFoundError:
            print("   (flake8 not found, skipping)")
    elif target.suffix in ['.js', '.ts', '.jsx', '.tsx']:
        # Try eslint
        try:
            subprocess.run(["npx", "eslint", str(target)], check=False, shell=True)
        except Exception:
            print("   (eslint failed, skipping)")
            
def run_indexer(target):
    print("\n📚 Updating Codebase Index...")
    # Assume navigator is at .agent/skills/codebase-navigator/scripts/navigator.py
    # We are running from project root usually?
    # Script location: .agent/skills/diff-applier/scripts/apply_patch.py
    # Navigator: ../../codebase-navigator/scripts/navigator.py
    
    base_dir = Path(__file__).resolve().parent.parent.parent
    navigator_script = base_dir / "codebase-navigator" / "scripts" / "navigator.py"
    
    if navigator_script.exists():
        try:
            subprocess.run(["python", str(navigator_script), "--incremental"], check=True)
            print("✅ Index updated.")
        except Exception as e:
            print(f"⚠️ Index update failed: {e}")
    else:
        print(f"⚠️ Navigator script not found at {navigator_script}")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("target_file")
    parser.add_argument("patch_file")
    args = parser.parse_args()
    
    apply_patch(args.target_file, args.patch_file)

if __name__ == "__main__":
    main()
