#!/usr/bin/env python3
"""
Team Learner — Scans conversation logs to extract coding habits and preferences.
Identifies repeated user directives and adds them as team rules.

Data sources:
  - Antigravity: ~/.gemini/antigravity/brain/<conversation-id>/.system_generated/logs/
  - Cursor: (future support)

Usage:
    python team_learner.py
    python team_learner.py --conversations ~/.gemini/antigravity/brain
    python team_learner.py --limit 10
"""

import argparse
import json
import os
import re
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from team_manager import get_active_team, get_team_dir, add_rule, load_team_json

GEMINI_DIR = Path.home() / ".gemini" / "antigravity" / "brain"

# Patterns that indicate user directives/preferences
DIRECTIVE_PATTERNS = [
    # Language preferences
    r"(?:always|please|must|should)\s+(?:write|use|code)\s+(?:in\s+)?(\w+)",
    # Style preferences
    r"(?:use|prefer|always use)\s+(camelCase|snake_case|PascalCase)",
    r"(?:use|prefer|always use)\s+(tailwind|sass|css modules|styled-components)",
    r"(?:use|prefer|always use)\s+(typescript|javascript|python)",
    # Explicit rules
    r"(?:always|never|must|should)\s+(.{10,60}?)(?:\.|$|!)",
    # Commit patterns
    r"(?:always|please)\s+(commit|push|git push|git commit)(.{0,30}?)(?:\.|$)",
    # Documentation preferences
    r"(?:write|add)\s+(?:docs?|documentation|comments?)\s+in\s+(\w+)",
]

# Known preference keywords to extract
PREFERENCE_KEYWORDS = {
    "english", "vietnamese", "tiếng anh", "tiếng việt",
    "camelcase", "snake_case", "pascalcase",
    "tailwind", "tailwindcss", "sass", "css modules",
    "typescript", "javascript", "python",
    "commit", "push", "deploy",
    "dark mode", "light mode",
    "responsive", "mobile-first",
}


def scan_conversation_logs(conversations_dir: Path, limit: int = 20) -> list[str]:
    """Scan conversation log files and extract user messages."""
    user_messages = []

    if not conversations_dir.exists():
        return user_messages

    # Find all conversation directories
    conv_dirs = sorted(
        [d for d in conversations_dir.iterdir() if d.is_dir()],
        key=lambda d: d.stat().st_mtime,
        reverse=True
    )[:limit]

    for conv_dir in conv_dirs:
        logs_dir = conv_dir / ".system_generated" / "logs"
        if not logs_dir.exists():
            continue

        for log_file in logs_dir.glob("*.txt"):
            try:
                content = log_file.read_text(encoding="utf-8", errors="ignore")
                # Extract user messages (lines that look like user input)
                for line in content.splitlines():
                    line = line.strip()
                    # Skip empty lines and system messages
                    if not line or len(line) < 10:
                        continue
                    # User messages tend to be shorter directives
                    if len(line) < 200:
                        user_messages.append(line.lower())
            except (OSError, UnicodeDecodeError):
                continue

    return user_messages


def extract_directives(messages: list[str]) -> Counter:
    """Extract repeated directives from user messages."""
    directives = Counter()

    for msg in messages:
        for pattern in DIRECTIVE_PATTERNS:
            matches = re.findall(pattern, msg, re.IGNORECASE)
            for match in matches:
                if isinstance(match, tuple):
                    match = " ".join(m for m in match if m).strip()
                directive = match.strip().rstrip(".,!;:")
                if len(directive) > 5 and len(directive) < 100:
                    directives[directive] += 1

        # Check for preference keywords
        for kw in PREFERENCE_KEYWORDS:
            if kw in msg:
                directives[f"preference:{kw}"] += 1

    return directives


def learn_from_conversations(conversations_dir: Path = None, limit: int = 20, quiet: bool = False):
    """Main learn function — scan conversations and update team rules."""
    active_team = get_active_team()
    if not active_team:
        if not quiet:
            print("❌ No active team. Create one: vibegravity team create <name>")
        return

    team_dir = get_team_dir(active_team)
    if not team_dir.exists():
        if not quiet:
            print(f"❌ Team '{active_team}' not found.")
        return

    # Determine conversations directory
    if conversations_dir is None:
        conversations_dir = GEMINI_DIR

    if not conversations_dir.exists():
        if not quiet:
            print(f"ℹ️  No conversation logs found at {conversations_dir}")
        return

    if not quiet:
        print(f"🔍 Scanning conversations in {conversations_dir}...")

    # Scan and extract
    messages = scan_conversation_logs(conversations_dir, limit)
    if not messages:
        if not quiet:
            print("ℹ️  No messages found to analyze.")
        return

    directives = extract_directives(messages)

    # Filter: only keep directives that appeared 2+ times
    repeated = {k: v for k, v in directives.items() if v >= 2}

    if not repeated:
        if not quiet:
            print("ℹ️  No repeated directives found (need 2+ occurrences).")
        return

    # Load existing rules to avoid duplicates
    rules_file = team_dir / "warm" / "rules.json"
    existing_rules = set()
    if rules_file.exists():
        rules_data = json.loads(rules_file.read_text(encoding="utf-8"))
        existing_rules = {r.get("text", "").lower() for r in rules_data.get("rules", [])}

    # Add new rules
    new_count = 0
    for directive, freq in sorted(repeated.items(), key=lambda x: -x[1]):
        # Clean up
        clean = directive.replace("preference:", "").strip()
        if clean.lower() in existing_rules:
            continue
        if not quiet:
            print(f"  📝 Found: \"{clean}\" (×{freq})")
        add_rule(active_team, clean, agent="global")
        new_count += 1

    if not quiet:
        if new_count > 0:
            print(f"\n✅ Added {new_count} new rules to team '{active_team}'.")
        else:
            print("ℹ️  All detected directives already exist as rules.")

    # Output for agent consumption
    if quiet:
        print(f"LEARNED={new_count}")


def main():
    parser = argparse.ArgumentParser(description="Team Learner — extract habits from conversations")
    parser.add_argument("--conversations", default=None, help="Path to conversation logs directory")
    parser.add_argument("--limit", type=int, default=20, help="Max conversations to scan")
    parser.add_argument("--quiet", action="store_true", help="Machine-readable output")
    args = parser.parse_args()

    conv_dir = Path(args.conversations) if args.conversations else None
    learn_from_conversations(conv_dir, args.limit, args.quiet)


if __name__ == "__main__":
    main()
