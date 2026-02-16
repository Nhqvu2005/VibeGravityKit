#!/usr/bin/env python3
"""
Codebase Navigator — Index and Search Codebase Symbols (Token Optimized).

Usage:
    python navigator.py --action index --path "./src"
    python navigator.py --action search --query "UserLogin"
    python navigator.py --action map
    python navigator.py --action outline              # Leader-friendly compact view
"""

import argparse
import json
import os
import re
from pathlib import Path

# Path to index file
INDEX_FILE = Path(__file__).parent.parent / "data" / "codebase_index.json"

# Regex patterns for symbols — captures full signature line
PATTERNS = {
    "python": [
        (r"^\s*(class\s+\w+[^:]*)", "class"),
        (r"^\s*(def\s+\w+\s*\([^)]*\)[^:]*)", "function"),
    ],
    "javascript": [
        (r"^\s*(class\s+\w+[^{]*)", "class"),
        (r"^\s*((?:async\s+)?function\s+\w+\s*\([^)]*\))", "function"),
        (r"^\s*((?:export\s+)?const\s+\w+\s*=\s*(?:async\s*)?\([^)]*\)\s*(?:=>)?)", "function"),
        (r"^\s*((?:export\s+)?(?:async\s+)?\w+\s*\([^)]*\)\s*\{)", "method"),
    ],
    "java": [
        (r"^\s*((?:public|private|protected)\s+class\s+\w+[^{]*)", "class"),
        (r"^\s*((?:public|private|protected)\s+interface\s+\w+[^{]*)", "interface"),
        (r"^\s*((?:public|private|protected)\s+\w+\s+\w+\s*\([^)]*\))", "method"),
    ],
    "csharp": [
        (r"^\s*((?:public|private|protected)\s+class\s+\w+[^{]*)", "class"),
        (r"^\s*((?:public|private|protected)\s+interface\s+\w+[^{]*)", "interface"),
        (r"^\s*((?:public|private|protected)\s+\w+\s+\w+\s*\([^)]*\))", "method"),
    ],
    "go": [
        (r"^(func\s+(?:\(\w+\s+\*?\w+\)\s+)?\w+\s*\([^)]*\)[^{]*)", "function"),
        (r"^(type\s+\w+\s+struct)", "struct"),
        (r"^(type\s+\w+\s+interface)", "interface"),
    ]
}

EXTENSIONS = {
    ".py": "python",
    ".js": "javascript",
    ".ts": "javascript",
    ".jsx": "javascript",
    ".tsx": "javascript",
    ".java": "java",
    ".cs": "csharp",
    ".go": "go"
}

IGNORED_DIRS = {
    "node_modules", ".git", "__pycache__", "dist", "build", "venv", "env", ".idea", ".vscode"
}

def load_index():
    if not INDEX_FILE.exists():
        return {"files": {}, "metadata": {}}
    with open(INDEX_FILE, "r", encoding="utf-8") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return {"files": {}, "metadata": {}}

def save_index(index):
    INDEX_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(INDEX_FILE, "w", encoding="utf-8") as f:
        json.dump(index, f, indent=2)

def index_codebase(root_path, incremental=False):
    index = load_index() if incremental else {"files": {}, "metadata": {}}
    if "files" not in index: index["files"] = {}
    if "metadata" not in index: index["metadata"] = {}
    
    root_path = Path(root_path)
    print(f"🔍 Indexing codebase at: {root_path} (Incremental: {incremental})")
    
    changes = {"updated": [], "removed": [], "added": []}
    current_files = set()
    
    # 1. Scan files
    for root, dirs, files in os.walk(root_path):
        dirs[:] = [d for d in dirs if d not in IGNORED_DIRS]
        
        for file in files:
            file_path = Path(root) / file
            rel_path = str(file_path.relative_to(root_path))
            ext = file_path.suffix.lower()
            
            if ext in EXTENSIONS:
                current_files.add(rel_path)
                mtime = file_path.stat().st_mtime
                
                # Check if modified
                last_mtime = index["metadata"].get(rel_path, 0)
                if incremental and mtime <= last_mtime and rel_path in index["files"]:
                    continue # Skip unchanged
                
                # Parse
                lang = EXTENSIONS[ext]
                symbols = []
                try:
                    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                        lines = f.readlines()
                    
                    for line_num, line in enumerate(lines, 1):
                        for pattern, sym_type in PATTERNS[lang]:
                            match = re.search(pattern, line)
                            if match:
                                signature = match.group(1).strip()
                                # Extract just the name for searching
                                name_match = re.search(r'(?:class|def|function|func|const|let|type)\s+(\w+)', signature)
                                name = name_match.group(1) if name_match else signature.split('(')[0].split()[-1]
                                symbols.append({
                                    "name": name,
                                    "signature": signature,
                                    "line": line_num,
                                    "type": sym_type
                                })
                    
                    index["files"][rel_path] = symbols
                    index["metadata"][rel_path] = mtime
                    
                    if rel_path in index["metadata"] and incremental:
                         changes["updated"].append(rel_path)
                    else:
                         changes["added"].append(rel_path)
                         
                    print(f"   Indexed: {rel_path} ({len(symbols)} symbols)")
                    
                except Exception as e:
                    print(f"   Error reading {file_path}: {e}")

    # 2. Cleanup removed files
    known_files = list(index["files"].keys())
    for f in known_files:
        if f not in current_files:
            del index["files"][f]
            if f in index["metadata"]: del index["metadata"][f]
            changes["removed"].append(f)
            print(f"   Removed: {f}")

    save_index(index)
    
    print("\n📊 Index Report:")
    if changes['added']: print(f"   + Added: {len(changes['added'])} files")
    if changes['updated']: print(f"   ~ Updated: {len(changes['updated'])} files")
    if changes['removed']: print(f"   - Removed: {len(changes['removed'])} files")
    print("✅ Indexing complete.")

def search_index(query):
    index = load_index()
    if not index or "files" not in index:
        print("❌ No index found. Run --action index first.")
        return

    results = []
    print(f"🔎 Searching for '{query}'...")
    
    for file_path, symbols in index.get("files", {}).items():
        # Match file name
        if query.lower() in file_path.lower():
            results.append(f"📄 File: {file_path}")
            
        # Match symbols by name or signature
        for sym in symbols:
            if query.lower() in sym["name"].lower() or query.lower() in sym.get("signature", "").lower():
                sig = sym.get("signature", sym["name"])
                results.append(f"   🔹 {sig} → {file_path}:{sym['line']}")
                
    if results:
        for r in results:
            print(r)
    else:
        print("   No matches found.")

def show_map():
    index = load_index()
    if not index or "files" not in index:
        print("❌ No index found. Run --action index first.")
        return

    print("\n🗺️ CODEBASE MAP:")
    for file_path, symbols in index.get("files", {}).items():
        print(f"\n📄 {file_path}")
        for sym in symbols:
             sig = sym.get("signature", sym["name"])
             print(f"   L{sym['line']}: {sig}")


def show_outline():
    """Leader-friendly compact outline — one line per file with symbols."""
    index = load_index()
    if not index or "files" not in index:
        print("❌ No index found. Run --action index first.")
        return

    total_files = len(index["files"])
    total_symbols = sum(len(s) for s in index["files"].values())
    print(f"📊 Codebase: {total_files} files, {total_symbols} symbols\n")

    for file_path, symbols in sorted(index.get("files", {}).items()):
        if not symbols:
            continue
        names = [f"{s['name']}:{s['line']}" for s in symbols]
        print(f"  {file_path} → {', '.join(names)}")


def main():
    parser = argparse.ArgumentParser(description="Codebase Navigator")
    parser.add_argument("--action", type=str, required=True, choices=["index", "search", "map", "outline"], help="Action")
    parser.add_argument("--path", type=str, default=".", help="Root path for indexing")
    parser.add_argument("--query", type=str, help="Search query")
    parser.add_argument("--incremental", action="store_true", help="Only update changed files")
    
    args = parser.parse_args()
    
    if args.action == "index":
        index_codebase(args.path, args.incremental)
    elif args.action == "search":
        if not args.query:
            print("Error: --query required for search")
        else:
            search_index(args.query)
    elif args.action == "map":
        show_map()
    elif args.action == "outline":
        show_outline()

if __name__ == "__main__":
    main()
