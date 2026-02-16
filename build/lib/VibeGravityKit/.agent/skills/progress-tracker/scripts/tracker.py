#!/usr/bin/env python3
"""
Progress Tracker — Parse task.md and generate progress report.

Usage:
    python tracker.py --task-file "path/to/task.md"
"""

import argparse
import json
import re
import sys
from pathlib import Path


def parse_args():
    parser = argparse.ArgumentParser(description="Progress Tracker")
    parser.add_argument("--task-file", type=str, required=True, help="Path to task.md file")
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    return parser.parse_args()


def parse_task_file(filepath):
    """Parse task.md and extract status of each task."""
    path = Path(filepath)
    if not path.exists():
        return {"error": f"File not found: {filepath}"}

    content = path.read_text(encoding="utf-8")
    lines = content.split("\n")

    tasks = {
        "completed": [],      # [x]
        "in_progress": [],     # [/]
        "pending": [],         # [ ]
    }
    current_section = ""

    for line in lines:
        stripped = line.strip()

        # Detect section headers
        if stripped.startswith("#"):
            current_section = stripped.lstrip("#").strip()
            continue

        # Parse task items
        match = re.match(r'^[\s-]*\[([ x/])\]\s*(.+)', stripped)
        if match:
            status_char = match.group(1)
            task_text = match.group(2).strip()
            task_info = {
                "text": task_text,
                "section": current_section
            }

            if status_char == "x":
                tasks["completed"].append(task_info)
            elif status_char == "/":
                tasks["in_progress"].append(task_info)
            else:
                tasks["pending"].append(task_info)

    total = len(tasks["completed"]) + len(tasks["in_progress"]) + len(tasks["pending"])
    progress = (len(tasks["completed"]) / total * 100) if total > 0 else 0

    return {
        "total": total,
        "completed": len(tasks["completed"]),
        "in_progress": len(tasks["in_progress"]),
        "pending": len(tasks["pending"]),
        "progress_percent": round(progress, 1),
        "details": tasks
    }


def print_readable(result):
    """Print progress report in a readable format."""
    if "error" in result:
        print(f"❌ {result['error']}")
        return

    pct = result["progress_percent"]
    bar_filled = int(pct / 5)
    bar = "█" * bar_filled + "░" * (20 - bar_filled)

    print("=" * 60)
    print("📊 PROGRESS REPORT")
    print("=" * 60)
    print(f"\n  [{bar}] {pct}%")
    print(f"\n  Total tasks:    {result['total']}")
    print(f"  ✅ Completed:   {result['completed']}")
    print(f"  🔄 In Progress: {result['in_progress']}")
    print(f"  ⏳ Pending:     {result['pending']}")

    if result["details"]["completed"]:
        print(f"\n{'─' * 60}")
        print("  ✅ COMPLETED:")
        for t in result["details"]["completed"]:
            section = f" [{t['section']}]" if t["section"] else ""
            print(f"    ✓ {t['text']}{section}")

    if result["details"]["in_progress"]:
        print(f"\n{'─' * 60}")
        print("  🔄 IN PROGRESS:")
        for t in result["details"]["in_progress"]:
            section = f" [{t['section']}]" if t["section"] else ""
            print(f"    → {t['text']}{section}")

    if result["details"]["pending"]:
        print(f"\n{'─' * 60}")
        print("  ⏳ NEXT UP:")
        for t in result["details"]["pending"]:
            section = f" [{t['section']}]" if t["section"] else ""
            print(f"    ○ {t['text']}{section}")

    print(f"\n{'=' * 60}")


if __name__ == "__main__":
    args = parse_args()
    result = parse_task_file(args.task_file)

    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print_readable(result)
