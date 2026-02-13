#!/usr/bin/env python3
"""
Release Manager — Changelog generation and version bumping.

Reads git history, groups commits by type (feat/fix/chore),
and manages semantic versioning.

Usage:
    python release.py --action changelog
    python release.py --action changelog --since "v2.0.0"
    python release.py --action bump --type minor
    python release.py --action version
"""

import argparse
import os
import re
import subprocess
import sys


def run_git(cmd):
    """Run a git command and return output."""
    try:
        result = subprocess.run(
            ["git"] + cmd,
            capture_output=True, text=True, timeout=10
        )
        return result.stdout.strip()
    except (subprocess.TimeoutExpired, FileNotFoundError):
        return ""


def get_current_version():
    """Read version from VERSION file or git tags."""
    version_files = [
        "VERSION",
        os.path.join(".agent", "..", "VERSION"),
    ]
    for vf in version_files:
        if os.path.exists(vf):
            with open(vf, "r") as f:
                return f.read().strip()

    # Fallback: latest git tag
    tag = run_git(["describe", "--tags", "--abbrev=0"])
    if tag:
        return tag.lstrip("v")
    return "0.0.0"


def bump_version(current, bump_type):
    """Bump semantic version."""
    parts = current.split(".")
    if len(parts) != 3:
        parts = ["0", "0", "0"]

    major, minor, patch = int(parts[0]), int(parts[1]), int(parts[2])

    if bump_type == "major":
        major += 1
        minor = 0
        patch = 0
    elif bump_type == "minor":
        minor += 1
        patch = 0
    elif bump_type == "patch":
        patch += 1

    return f"{major}.{minor}.{patch}"


def parse_commits(since=None):
    """Parse git log into categorized commits."""
    cmd = ["log", "--pretty=format:%h|%s|%an|%ad", "--date=short"]
    if since:
        cmd.append(f"{since}..HEAD")
    else:
        cmd.extend(["-n", "50"])

    output = run_git(cmd)
    if not output:
        return {}

    categories = {
        "feat": [],
        "fix": [],
        "docs": [],
        "style": [],
        "refactor": [],
        "test": [],
        "chore": [],
        "other": []
    }

    for line in output.split("\n"):
        parts = line.split("|", 3)
        if len(parts) < 2:
            continue
        hash_val, message = parts[0], parts[1]
        author = parts[2] if len(parts) > 2 else ""
        date = parts[3] if len(parts) > 3 else ""

        # Parse conventional commit type
        match = re.match(r'^(\w+)(?:\(.*?\))?[!:]?\s*(.*)$', message)
        if match:
            commit_type = match.group(1).lower()
            description = match.group(2) or message
        else:
            commit_type = "other"
            description = message

        if commit_type not in categories:
            commit_type = "other"

        categories[commit_type].append({
            "hash": hash_val,
            "message": description,
            "author": author,
            "date": date
        })

    return {k: v for k, v in categories.items() if v}


def format_changelog(categories, version=None):
    """Format categorized commits into markdown changelog."""
    type_labels = {
        "feat": "✨ Features",
        "fix": "🐛 Bug Fixes",
        "docs": "📚 Documentation",
        "style": "🎨 Styling",
        "refactor": "♻️ Refactoring",
        "test": "🧪 Testing",
        "chore": "🔧 Chores",
        "other": "📝 Other"
    }

    lines = []
    if version:
        lines.append(f"## v{version}")
        lines.append("")

    for cat_type, commits in categories.items():
        label = type_labels.get(cat_type, cat_type)
        lines.append(f"### {label}")
        for commit in commits:
            lines.append(f"- {commit['message']} (`{commit['hash']}`)")
        lines.append("")

    total = sum(len(v) for v in categories.values())
    lines.append(f"**Total: {total} commits**")
    return "\n".join(lines)


def do_bump(bump_type):
    """Bump version and update VERSION file."""
    current = get_current_version()
    new_version = bump_version(current, bump_type)

    # Update VERSION file
    version_file = "VERSION"
    if not os.path.exists(version_file):
        # Look in common locations
        for candidate in ["VERSION", "version.txt"]:
            if os.path.exists(candidate):
                version_file = candidate
                break

    with open(version_file, "w") as f:
        f.write(new_version + "\n")

    print(f"Version bumped: {current} → {new_version}")
    print(f"Updated: {version_file}")
    return new_version


def main():
    parser = argparse.ArgumentParser(description="Release Manager — Changelog & Versioning")
    parser.add_argument("--action", "-a", required=True,
                        choices=["changelog", "bump", "version"],
                        help="Action to perform")
    parser.add_argument("--since", help="Git ref to start changelog from (tag or commit)")
    parser.add_argument("--type", dest="bump_type", default="patch",
                        choices=["major", "minor", "patch"],
                        help="Version bump type (default: patch)")
    parser.add_argument("--format", "-f", default="text",
                        choices=["text", "json"],
                        help="Output format")

    args = parser.parse_args()

    if args.action == "version":
        version = get_current_version()
        print(f"Current version: v{version}")

    elif args.action == "changelog":
        categories = parse_commits(args.since)
        if not categories:
            print("No commits found.")
            return
        changelog = format_changelog(categories)
        print(changelog)

    elif args.action == "bump":
        do_bump(args.bump_type)


if __name__ == "__main__":
    main()
