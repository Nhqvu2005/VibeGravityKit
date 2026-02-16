#!/usr/bin/env python3
"""
Test Generator — Generate Test Skeletons (Zero Token) with Smart Mode.

Usage:
    # Single file (original behavior)
    python gen_skeleton.py src/utils.py > tests/test_utils.py

    # From codebase index — generate tests for ALL indexed symbols
    python gen_skeleton.py --from-index > tests/test_all.py
    python gen_skeleton.py --from-index --style smart > tests/test_all.py

    # Coverage report — show which functions are tested vs untested
    python gen_skeleton.py --from-index --coverage-report

    # Smart mode on single file
    python gen_skeleton.py src/utils.py --style smart > tests/test_utils.py
"""

import argparse
import json
import re
import sys
from pathlib import Path

INDEX_FILE = Path(__file__).parent.parent.parent / "codebase-navigator" / "data" / "codebase_index.json"
EDGE_CASES_FILE = Path(__file__).parent.parent / "data" / "edge_cases.json"


# ──────────────────── TYPE HINT ANALYSIS ────────────────────

def parse_type_hint(hint: str) -> str:
    """Normalize type hint string."""
    hint = hint.strip()
    # Remove Optional[], Union[], etc.
    if hint.startswith("Optional["):
        hint = hint[9:-1]
    return hint

def infer_test_values(param_name: str, type_hint: str = "") -> dict:
    """Generate test values based on parameter name and type hint."""
    hint = type_hint.lower() if type_hint else ""
    name = param_name.lower()

    # String types
    if hint in ("str", "string") or any(k in name for k in ("name", "text", "title", "desc", "msg", "email", "url", "path", "query")):
        return {
            "valid": '"test_value"',
            "empty": '""',
            "null": "None",
            "edge": '"a" * 10000',
            "special": '"<script>alert(1)</script>"',
            "type": "str"
        }

    # Numeric types
    if hint in ("int", "float", "number") or any(k in name for k in ("count", "num", "size", "length", "amount", "price", "id", "age", "limit", "offset", "page")):
        return {
            "valid": "42",
            "zero": "0",
            "negative": "-1",
            "null": "None",
            "edge": "2**31 - 1",
            "type": "int"
        }

    # Boolean types
    if hint in ("bool", "boolean") or any(k in name for k in ("is_", "has_", "can_", "should_", "enable", "active", "flag")):
        return {
            "valid": "True",
            "false": "False",
            "null": "None",
            "type": "bool"
        }

    # List/Array types
    if hint.startswith(("list", "array", "sequence")) or any(k in name for k in ("items", "list", "array", "data", "records", "results")):
        return {
            "valid": "[1, 2, 3]",
            "empty": "[]",
            "single": "[1]",
            "null": "None",
            "large": "list(range(10000))",
            "type": "list"
        }

    # Dict types
    if hint.startswith("dict") or any(k in name for k in ("config", "options", "settings", "params", "kwargs", "headers", "payload")):
        return {
            "valid": '{"key": "value"}',
            "empty": "{}",
            "null": "None",
            "nested": '{"a": {"b": {"c": 1}}}',
            "type": "dict"
        }

    # Default — unknown type
    return {
        "valid": '"test_value"',
        "null": "None",
        "type": "unknown"
    }


# ──────────────────── SIGNATURE PARSING ────────────────────

def parse_params_from_signature(signature: str) -> list[dict]:
    """Extract parameters from function signature."""
    # Match content inside parentheses
    match = re.search(r'\(([^)]*)\)', signature)
    if not match:
        return []

    params_str = match.group(1).strip()
    if not params_str:
        return []

    params = []
    for part in params_str.split(","):
        part = part.strip()
        if not part or part in ("self", "cls", "*args", "**kwargs"):
            continue

        # Handle type hints: param: type = default
        name = part.split(":")[0].split("=")[0].strip()
        type_hint = ""
        if ":" in part:
            type_hint = part.split(":")[1].split("=")[0].strip()

        has_default = "=" in part

        if name and name not in ("self", "cls"):
            params.append({
                "name": name,
                "type_hint": type_hint,
                "has_default": has_default,
                "test_values": infer_test_values(name, type_hint)
            })

    return params


# ──────────────────── PYTHON TEST GENERATION ────────────────────

def generate_python_tests_skeleton(content: str):
    """Original skeleton mode — simple stubs."""
    funcs = re.findall(r'def\s+([a-zA-Z_0-9]+)\s*\(', content)

    print("import pytest")
    print("from src import module  # Update import\n")

    for f in funcs:
        if f.startswith('_'):
            continue
        print(f"def test_{f}():")
        print(f"    # TODO: Implement test for {f}")
        print(f"    assert True\n")


def generate_python_tests_smart(content: str, file_path: str = ""):
    """Smart mode — real test cases with edge cases."""
    # Parse all functions with full signatures
    functions = re.findall(r'(def\s+[a-zA-Z_0-9]+\s*\([^)]*\)[^:]*)', content)

    module_name = Path(file_path).stem if file_path else "module"

    print("import pytest")
    print(f"# from src.{module_name} import *  # Update import path\n")

    for sig in functions:
        name_match = re.search(r'def\s+([a-zA-Z_0-9]+)', sig)
        if not name_match:
            continue
        func_name = name_match.group(1)
        if func_name.startswith('_'):
            continue

        params = parse_params_from_signature(sig)

        print(f"\nclass Test_{func_name}:")
        print(f'    """Tests for {func_name}"""')

        # Test 1: Valid input
        valid_args = ", ".join(p["test_values"]["valid"] for p in params) if params else ""
        print(f"\n    def test_{func_name}_valid_input(self):")
        print(f"        result = {func_name}({valid_args})")
        print(f"        assert result is not None")

        # Test 2: Edge cases per parameter
        for p in params:
            tv = p["test_values"]

            # Null test
            if "null" in tv:
                print(f"\n    def test_{func_name}_{p['name']}_null(self):")
                print(f"        with pytest.raises((TypeError, ValueError)):")
                print(f"            {func_name}({_replace_param(params, p['name'], tv['null'])})")

            # Empty test
            if "empty" in tv:
                print(f"\n    def test_{func_name}_{p['name']}_empty(self):")
                print(f"        result = {func_name}({_replace_param(params, p['name'], tv['empty'])})")
                print(f"        assert result is not None  # Verify handles empty gracefully")

            # Zero/negative for numbers
            if tv.get("type") == "int":
                print(f"\n    def test_{func_name}_{p['name']}_zero(self):")
                print(f"        result = {func_name}({_replace_param(params, p['name'], '0')})")
                print(f"        assert result is not None")

                print(f"\n    def test_{func_name}_{p['name']}_negative(self):")
                print(f"        result = {func_name}({_replace_param(params, p['name'], '-1')})")
                print(f"        assert result is not None  # Or raises ValueError")

            # Boundary for numbers
            if "edge" in tv and tv.get("type") == "int":
                print(f"\n    def test_{func_name}_{p['name']}_boundary(self):")
                print(f"        result = {func_name}({_replace_param(params, p['name'], tv['edge'])})")
                print(f"        assert result is not None  # Verify handles large values")

            # Special chars for strings
            if "special" in tv:
                print(f"\n    def test_{func_name}_{p['name']}_special_chars(self):")
                print(f"        result = {func_name}({_replace_param(params, p['name'], tv['special'])})")
                print(f"        assert result is not None  # XSS/injection safety")

            # Large input
            if "large" in tv:
                print(f"\n    def test_{func_name}_{p['name']}_large_input(self):")
                print(f"        result = {func_name}({_replace_param(params, p['name'], tv['large'])})")
                print(f"        assert result is not None  # Performance/memory check")

        print()


def _replace_param(params: list, target_name: str, target_value: str) -> str:
    """Build argument string, replacing one param with a test value."""
    args = []
    for p in params:
        if p["name"] == target_name:
            args.append(target_value)
        else:
            args.append(p["test_values"]["valid"])
    return ", ".join(args)


# ──────────────────── JS/TS TEST GENERATION ────────────────────

def generate_js_tests_skeleton(content: str):
    """Original skeleton mode."""
    funcs = re.findall(r'function\s+([a-zA-Z_0-9]+)', content)
    arrow_funcs = re.findall(r'(?:const|let|var)\s+([a-zA-Z_0-9]+)\s*=\s*\(', content)
    all_funcs = funcs + arrow_funcs

    print("import { describe, it, expect } from 'vitest';\n")

    for f in all_funcs:
        print(f"describe('{f}', () => {{")
        print(f"  it('should work', () => {{")
        print(f"    // TODO: Implement test for {f}")
        print(f"    expect(true).toBe(true);")
        print(f"  }});")
        print(f"}});\n")


def generate_js_tests_smart(content: str, file_path: str = ""):
    """Smart mode for JS/TS."""
    funcs = re.findall(r'(?:async\s+)?function\s+([a-zA-Z_0-9]+)\s*\(([^)]*)\)', content)
    arrow_funcs = re.findall(r'(?:const|let|var)\s+([a-zA-Z_0-9]+)\s*=\s*(?:async\s*)?\(([^)]*)\)', content)
    all_funcs = funcs + arrow_funcs

    module_name = Path(file_path).stem if file_path else "module"

    print("import { describe, it, expect } from 'vitest';")
    print(f"// import {{ ... }} from './{module_name}';\n")

    for func_name, params_str in all_funcs:
        params = [p.strip().split(":")[0].split("=")[0].strip()
                  for p in params_str.split(",") if p.strip()]

        print(f"describe('{func_name}', () => {{")

        # Valid input
        print(f"  it('should return valid result for normal input', () => {{")
        print(f"    const result = {func_name}({', '.join(_js_test_value(p) for p in params)});")
        print(f"    expect(result).toBeDefined();")
        print(f"  }});\n")

        # Null/undefined
        for p in params:
            print(f"  it('should handle {p} as null', () => {{")
            print(f"    expect(() => {func_name}({', '.join('null' if pp == p else _js_test_value(pp) for pp in params)})).toThrow();")
            print(f"  }});\n")

            print(f"  it('should handle {p} as undefined', () => {{")
            print(f"    expect(() => {func_name}({', '.join('undefined' if pp == p else _js_test_value(pp) for pp in params)})).toThrow();")
            print(f"  }});\n")

        # Empty string
        for p in params:
            if any(k in p.lower() for k in ("name", "text", "title", "email", "url", "str", "msg", "query")):
                print(f"  it('should handle empty {p}', () => {{")
                print(f"    const result = {func_name}({', '.join('\"\"' if pp == p else _js_test_value(pp) for pp in params)});")
                print(f"    expect(result).toBeDefined();")
                print(f"  }});\n")

        # XSS test
        for p in params:
            if any(k in p.lower() for k in ("name", "text", "title", "input", "html", "content", "query")):
                print(f"  it('should sanitize {p} against XSS', () => {{")
                print(f"    const result = {func_name}({', '.join('\"<script>alert(1)</script>\"' if pp == p else _js_test_value(pp) for pp in params)});")
                print(f"    expect(String(result)).not.toContain('<script>');")
                print(f"  }});\n")

        print(f"}});\n")


def _js_test_value(param_name: str) -> str:
    """Generate a JS test value based on parameter name."""
    name = param_name.lower()
    if any(k in name for k in ("id", "count", "num", "size", "limit", "page", "index", "age", "amount")):
        return "42"
    if any(k in name for k in ("flag", "is_", "has_", "enable", "active", "bool")):
        return "true"
    if any(k in name for k in ("items", "list", "arr", "data", "records")):
        return "[1, 2, 3]"
    if any(k in name for k in ("config", "options", "settings", "params", "headers")):
        return "{ key: 'value' }"
    if any(k in name for k in ("callback", "fn", "handler", "func")):
        return "() => {}"
    return "'test_value'"


# ──────────────────── FROM-INDEX MODE ────────────────────

def load_index() -> dict:
    """Load codebase index from codebase-navigator."""
    if not INDEX_FILE.exists():
        print(f"❌ No codebase index found at: {INDEX_FILE}", file=sys.stderr)
        print("   Run first: python .agent/skills/codebase-navigator/scripts/navigator.py --action index --path .", file=sys.stderr)
        return {}
    with open(INDEX_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def generate_from_index(style: str = "skeleton"):
    """Read codebase index and generate tests for ALL symbols."""
    index = load_index()
    if not index:
        return

    files = index.get("files", {})
    total_symbols = sum(len(syms) for syms in files.values())
    total_funcs = sum(1 for syms in files.values() for s in syms if s["type"] in ("function", "method"))

    print(f"# Auto-generated tests from codebase index", file=sys.stderr)
    print(f"# Files: {len(files)}, Symbols: {total_symbols}, Functions: {total_funcs}", file=sys.stderr)

    for file_path, symbols in sorted(files.items()):
        funcs = [s for s in symbols if s["type"] in ("function", "method")]
        if not funcs:
            continue

        ext = Path(file_path).suffix.lower()

        # Read actual file content for smart analysis
        actual_path = Path(file_path)
        content = ""
        if actual_path.exists() and style == "smart":
            try:
                content = actual_path.read_text(encoding="utf-8", errors="ignore")
            except Exception:
                pass

        print(f"\n# {'='*60}")
        print(f"# Tests for: {file_path}")
        print(f"# Symbols: {len(funcs)} functions/methods")
        print(f"# {'='*60}\n")

        if ext == ".py":
            if style == "smart" and content:
                generate_python_tests_smart(content, file_path)
            else:
                # Generate from index signatures
                _generate_python_from_symbols(funcs, file_path)
        elif ext in (".js", ".ts", ".jsx", ".tsx"):
            if style == "smart" and content:
                generate_js_tests_smart(content, file_path)
            else:
                _generate_js_from_symbols(funcs, file_path)


def _generate_python_from_symbols(symbols: list, file_path: str):
    """Generate Python test stubs from index symbols."""
    module = Path(file_path).stem
    print(f"# from {module} import *  # Update import\n")

    for sym in symbols:
        name = sym["name"]
        sig = sym.get("signature", name)
        params = parse_params_from_signature(sig)

        print(f"def test_{name}():")
        if params:
            valid_args = ", ".join(p["test_values"]["valid"] for p in params)
            print(f"    result = {name}({valid_args})")
            print(f"    assert result is not None")
        else:
            print(f"    # TODO: test {name}")
            print(f"    assert True")

        # Null test for each param
        for p in params:
            print(f"\ndef test_{name}_{p['name']}_null():")
            print(f"    with pytest.raises((TypeError, ValueError)):")
            print(f"        {name}({_replace_param(params, p['name'], 'None')})")

        print()


def _generate_js_from_symbols(symbols: list, file_path: str):
    """Generate JS test stubs from index symbols."""
    module = Path(file_path).stem
    print(f"// import {{ ... }} from './{module}';\n")

    for sym in symbols:
        name = sym["name"]
        print(f"describe('{name}', () => {{")
        print(f"  it('should work correctly', () => {{")
        print(f"    // TODO: test {name}")
        print(f"    expect(true).toBe(true);")
        print(f"  }});")
        print(f"}});\n")


# ──────────────────── COVERAGE REPORT ────────────────────

def coverage_report():
    """Show which functions have tests vs untested."""
    index = load_index()
    if not index:
        return

    files = index.get("files", {})

    # Find existing test files
    test_files_content = {}
    for test_dir in [Path("tests"), Path("test"), Path("__tests__"), Path("src")]:
        if test_dir.exists():
            for tf in test_dir.rglob("test_*.*"):
                try:
                    test_files_content[str(tf)] = tf.read_text(encoding="utf-8", errors="ignore")
                except Exception:
                    pass
            for tf in test_dir.rglob("*.test.*"):
                try:
                    test_files_content[str(tf)] = tf.read_text(encoding="utf-8", errors="ignore")
                except Exception:
                    pass
            for tf in test_dir.rglob("*.spec.*"):
                try:
                    test_files_content[str(tf)] = tf.read_text(encoding="utf-8", errors="ignore")
                except Exception:
                    pass

    all_test_content = "\n".join(test_files_content.values()).lower()

    print("📊 TEST COVERAGE REPORT")
    print("=" * 60)

    total_funcs = 0
    tested_funcs = 0
    untested = []

    for file_path, symbols in sorted(files.items()):
        funcs = [s for s in symbols if s["type"] in ("function", "method")]
        if not funcs:
            continue

        file_tested = 0
        file_untested = []

        for sym in funcs:
            total_funcs += 1
            name = sym["name"].lower()
            # Check if test exists: test_funcname, funcname.test, describe('funcname'
            if (f"test_{name}" in all_test_content or
                f"'{name}'" in all_test_content or
                f'"{name}"' in all_test_content):
                tested_funcs += 1
                file_tested += 1
            else:
                file_untested.append(sym)
                untested.append((file_path, sym))

        status = "✅" if not file_untested else "⚠️"
        coverage = f"{file_tested}/{len(funcs)}"
        print(f"\n{status} {file_path} ({coverage} tested)")
        for sym in file_untested:
            print(f"   ❌ {sym.get('signature', sym['name'])} (line {sym['line']})")

    # Summary
    pct = (tested_funcs / total_funcs * 100) if total_funcs > 0 else 0
    print(f"\n{'=' * 60}")
    print(f"📈 Coverage: {tested_funcs}/{total_funcs} functions ({pct:.0f}%)")
    print(f"❌ Untested: {len(untested)} functions")

    if pct < 60:
        print("⚠️  Coverage below 60% — needs improvement!")
    elif pct < 80:
        print("🟡 Coverage OK but could be better (target: 80%+)")
    else:
        print("✅ Good coverage!")


# ──────────────────── MAIN ────────────────────

def main():
    parser = argparse.ArgumentParser(description="Test Generator — Smart Test Skeletons")
    parser.add_argument("file", nargs="?", help="Source file to generate tests for")
    parser.add_argument("--from-index", action="store_true",
                        help="Generate tests for ALL functions in codebase index")
    parser.add_argument("--style", choices=["skeleton", "smart"], default="skeleton",
                        help="skeleton: simple stubs | smart: real test cases with edge cases")
    parser.add_argument("--coverage-report", action="store_true",
                        help="Show coverage report: tested vs untested functions")

    args = parser.parse_args()

    # Coverage report mode
    if args.coverage_report:
        coverage_report()
        return

    # From index mode
    if args.from_index:
        generate_from_index(args.style)
        return

    # Single file mode (original)
    if not args.file:
        print("Error: provide a source file or use --from-index")
        return

    p = Path(args.file)
    if not p.exists():
        print(f"Error: file not found: {p}")
        return

    content = p.read_text(encoding="utf-8", errors="ignore")

    if p.suffix == ".py":
        if args.style == "smart":
            generate_python_tests_smart(content, str(p))
        else:
            generate_python_tests_skeleton(content)
    elif p.suffix in (".js", ".ts", ".jsx", ".tsx"):
        if args.style == "smart":
            generate_js_tests_smart(content, str(p))
        else:
            generate_js_tests_skeleton(content)
    else:
        print(f"// No test generator for {p.suffix}")


if __name__ == "__main__":
    main()
