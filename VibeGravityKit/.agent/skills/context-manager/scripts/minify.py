#!/usr/bin/env python3
"""
Context Manager — Minify code for LLM Context.

Usage:
    python minify.py <file_path> [--remove-comments] [--remove-empty-lines]
"""

import argparse
import re
import sys
from pathlib import Path

def remove_comments_python(source):
    # Remove single line comments
    source = re.sub(r'#.*', '', source)
    # Remove docstrings (simple approximation, not perfect)
    # source = re.sub(r'""".*?"""', '', source, flags=re.DOTALL) 
    # source = re.sub(r"'''.*?'''", '', source, flags=re.DOTALL)
    # Docstring removal via regex is dangerous, skipping for safety
    return source

def remove_comments_js(source):
    # Remove // comments
    source = re.sub(r'//.*', '', source)
    # Remove /* */ comments
    source = re.sub(r'/\*.*?\*/', '', source, flags=re.DOTALL)
    return source

def minify_file(file_path, remove_comments=True, remove_empty=True):
    path = Path(file_path)
    if not path.exists():
        print(f"Error: File {file_path} not found.")
        sys.exit(1)

    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()

    original_len = len(content)

    if remove_comments:
        if path.suffix in ['.py']:
            content = remove_comments_python(content)
        elif path.suffix in ['.js', '.ts', '.jsx', '.tsx', '.css', '.java', '.c', '.cpp']:
            content = remove_comments_js(content)
    
    lines = content.split('\n')
    cleaned_lines = []
    for line in lines:
        stripped = line.strip()
        if remove_empty and not stripped:
            continue
        # Preserve indentation but maybe reduce it? For now, keep indentation logic simple
        # Just creating a "dense" version
        cleaned_lines.append(line) # Keep indentation for readability/python correctness

    final_content = "\n".join(cleaned_lines)
    
    # Remove multi-line empty blocks again just in case
    if remove_empty:
        final_content = re.sub(r'\n\s*\n', '\n', final_content)

    new_len = len(final_content)
    saved = original_len - new_len
    percent = (saved / original_len) * 100 if original_len > 0 else 0

    print(f"📉 Minified {path.name}: {original_len} -> {new_len} chars (Saved {percent:.1f}%)")
    print("-" * 40)
    print(final_content)
    print("-" * 40)

def main():
    parser = argparse.ArgumentParser(description="Minify code for LLM context")
    parser.add_argument("file", help="File to minify")
    parser.add_argument("--no-comments", action="store_false", dest="remove_comments", help="Keep comments")
    parser.add_argument("--no-empty", action="store_false", dest="remove_empty", help="Keep empty lines")
    
    args = parser.parse_args()
    minify_file(args.file, args.remove_comments, args.remove_empty)

if __name__ == "__main__":
    main()
