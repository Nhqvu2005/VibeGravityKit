#!/usr/bin/env python3
"""
Code Reviewer — Zero-token regex-based code quality scanner.

Scans source files for anti-patterns, naming issues, security risks,
and best practices violations.

Usage:
    python reviewer.py --path "src/" --action scan
    python reviewer.py --path "src/api.py" --action naming
    python reviewer.py --path "src/" --action security
"""

import argparse
import json
import os
import re
import sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
RULES_FILE = os.path.join(SCRIPT_DIR, "..", "data", "review_rules.json")

EXTENSIONS = {
    ".py", ".js", ".ts", ".tsx", ".jsx", ".java", ".go",
    ".rb", ".php", ".cs", ".rs", ".swift", ".kt"
}


def load_rules():
    """Load review rules from JSON."""
    with open(RULES_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def find_files(path):
    """Find all source code files recursively."""
    files = []
    if os.path.isfile(path):
        return [path]
    for root, dirs, filenames in os.walk(path):
        # Skip common non-source directories
        dirs[:] = [d for d in dirs if d not in {
            "node_modules", ".git", "__pycache__", "venv", ".venv",
            "dist", "build", ".next", "coverage", ".agent"
        }]
        for fname in filenames:
            ext = os.path.splitext(fname)[1]
            if ext in EXTENSIONS:
                files.append(os.path.join(root, fname))
    return files


def scan_file(filepath, rules, action="scan"):
    """Scan a single file against rules."""
    issues = []
    try:
        with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
            lines = f.readlines()
    except (IOError, OSError):
        return issues

    for i, line in enumerate(lines, 1):
        stripped = line.strip()
        if not stripped or stripped.startswith("#") or stripped.startswith("//"):
            continue

        for rule in rules:
            if action != "scan" and rule.get("category") != action:
                continue
            pattern = rule.get("pattern", "")
            if not pattern:
                continue
            try:
                if re.search(pattern, line, re.IGNORECASE):
                    # Check exclusion patterns
                    exclude = rule.get("exclude_pattern")
                    if exclude and re.search(exclude, line, re.IGNORECASE):
                        continue
                    issues.append({
                        "file": filepath,
                        "line": i,
                        "severity": rule.get("severity", "info"),
                        "rule": rule.get("id", "unknown"),
                        "category": rule.get("category", "general"),
                        "message": rule.get("message", "Issue detected"),
                        "suggestion": rule.get("suggestion", ""),
                        "snippet": stripped[:120]
                    })
            except re.error:
                continue
    return issues


def calculate_score(issues):
    """Calculate overall quality score based on issues."""
    if not issues:
        return "A"
    critical = sum(1 for i in issues if i["severity"] == "critical")
    warning = sum(1 for i in issues if i["severity"] == "warning")
    if critical > 5:
        return "F"
    elif critical > 2:
        return "D"
    elif critical > 0 or warning > 10:
        return "C"
    elif warning > 3:
        return "B"
    return "A"


def format_report(issues, files_scanned):
    """Format issues into a structured report."""
    severity_order = {"critical": 0, "warning": 1, "info": 2}
    issues.sort(key=lambda x: severity_order.get(x["severity"], 3))

    critical = [i for i in issues if i["severity"] == "critical"]
    warnings = [i for i in issues if i["severity"] == "warning"]
    info = [i for i in issues if i["severity"] == "info"]

    report = {
        "summary": {
            "files_scanned": files_scanned,
            "total_issues": len(issues),
            "critical": len(critical),
            "warnings": len(warnings),
            "info": len(info),
            "quality_score": calculate_score(issues)
        },
        "issues": {
            "critical": critical[:20],
            "warning": warnings[:20],
            "info": info[:10]
        }
    }
    return report


def main():
    parser = argparse.ArgumentParser(description="Code Reviewer — Zero-token code quality scanner")
    parser.add_argument("--path", "-p", required=True, help="Path to scan (file or directory)")
    parser.add_argument("--action", "-a", default="scan",
                        choices=["scan", "naming", "security", "performance"],
                        help="Type of review (default: scan = all)")
    parser.add_argument("--format", "-f", default="text", choices=["text", "json"],
                        help="Output format (default: text)")
    args = parser.parse_args()

    if not os.path.exists(args.path):
        print(f"Error: Path not found: {args.path}", file=sys.stderr)
        sys.exit(1)

    rules_data = load_rules()
    all_rules = rules_data.get("rules", [])

    files = find_files(args.path)
    if not files:
        print("No source files found.")
        return

    all_issues = []
    for filepath in files:
        issues = scan_file(filepath, all_rules, args.action)
        all_issues.extend(issues)

    report = format_report(all_issues, len(files))

    if args.format == "json":
        print(json.dumps(report, indent=2, ensure_ascii=False))
    else:
        # Text format
        s = report["summary"]
        print(f"\n📝 Code Review Report")
        print(f"{'='*50}")
        print(f"Files scanned: {s['files_scanned']}")
        print(f"Quality Score: {s['quality_score']}")
        print(f"Issues: {s['total_issues']} ({s['critical']} critical, {s['warnings']} warnings, {s['info']} info)")

        for severity in ["critical", "warning", "info"]:
            items = report["issues"].get(severity, [])
            if not items:
                continue
            icon = {"critical": "🔴", "warning": "🟡", "info": "🔵"}[severity]
            print(f"\n{icon} {severity.upper()} ({len(items)})")
            for item in items:
                rel_path = os.path.relpath(item["file"])
                print(f"  [{rel_path}:{item['line']}] {item['message']}")
                if item.get("suggestion"):
                    print(f"    → {item['suggestion']}")


if __name__ == "__main__":
    main()
