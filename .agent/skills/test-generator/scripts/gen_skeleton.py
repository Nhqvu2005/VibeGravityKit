#!/usr/bin/env python3
"""
Test Generator — Generate Test Skeletons (Zero Token).

Usage:
    python gen_skeleton.py <src_file>
"""

import argparse
import re
from pathlib import Path

def generate_python_tests(content):
    # Find functions: def my_func(...):
    funcs = re.findall(r'def\s+([a-zA-Z_0-9]+)\s*\(', content)
    
    print("import pytest")
    print("from src import module  # Update import\n")
    
    for f in funcs:
        if f.startswith('_'): continue
        print(f"def test_{f}():")
        print(f"    # TODO: Implement test for {f}")
        print(f"    assert True\n")

def generate_js_tests(content):
    # Find functions: function myFunc() or const myFunc = ...
    funcs = re.findall(r'function\s+([a-zA-Z_0-9]+)', content)
    arrow_funcs = re.findall(r'(?:const|let|var)\s+([a-zA-Z_0-9]+)\s*=\s*\(', content)
    
    all_funcs = funcs + arrow_funcs
    
    print("import { expect, test } from 'vitest';\n")
    
    for f in all_funcs:
        print(f"test('{f} should work', () => {{")
        print(f"  // TODO: Implement test for {f}")
        print(f"  expect(true).toBe(true);")
        print(f"}});\n")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("file")
    args = parser.parse_args()
    
    p = Path(args.file)
    if not p.exists():
        return
        
    with open(p, 'r', encoding='utf-8') as f:
        content = f.read()
        
    if p.suffix == '.py':
        generate_python_tests(content)
    elif p.suffix in ['.js', '.ts', '.jsx', '.tsx']:
        generate_js_tests(content)
    else:
        print(f"// No test generator for {p.suffix}")

if __name__ == "__main__":
    main()
