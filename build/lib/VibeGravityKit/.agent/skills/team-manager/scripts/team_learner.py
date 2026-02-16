#!/usr/bin/env python3
"""
Team Learner — Extracts coding habits and preferences to update team profile.

Since conversation logs are not stored as accessible files, this script works
by analyzing the CURRENT project's code and artifacts to detect patterns.

Data sources (what we CAN access):
  1. Project source code — via team_scanner.py (detect code style)
  2. .agent/brain/ artifacts — task.md, implementation_plan.md, etc.
  3. Journal entries — .agent/brain/journal/ (if journal-manager created entries)
  4. Explicit directives — passed via --directive flag (leader calls this)

The LEADER/QUICKSTART workflows call this script passively:
  - On plan confirmation → scan code + extract from artifacts
  - On phase completion → leader passes observed directives via --directive

Usage:
    # Passive (called by leader at plan confirmation):
    python team_learner.py --scan-project .

    # Leader passes a specific directive it observed:
    python team_learner.py --directive "write docs in English"
    python team_learner.py --directive "always use Tailwind" --agent frontend-dev

    # Scan project artifacts for preferences:
    python team_learner.py --scan-artifacts .agent/brain

    # Full learn (code + artifacts):
    python team_learner.py --scan-project . --scan-artifacts .agent/brain

    # Quiet mode (for agent consumption):
    python team_learner.py --scan-project . --quiet
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
from team_scanner import scan_project, encode_dna


def extract_from_artifacts(brain_dir: Path) -> list[str]:
    """Extract preferences from .agent/brain/ artifacts (plans, tasks, etc.)."""
    directives = []

    # Read implementation plans — often contain user-decided tech choices
    for md_file in brain_dir.glob("*.md"):
        try:
            content = md_file.read_text(encoding="utf-8", errors="ignore")
            # Look for explicit user decisions/preferences in plans
            for line in content.splitlines():
                line = line.strip()
                # Lines that look like rules or decisions
                if re.match(r'^[-*]\s+(always|never|must|should|prefer|use)\s', line, re.IGNORECASE):
                    clean = re.sub(r'^[-*]\s+', '', line).strip()
                    if 10 < len(clean) < 100:
                        directives.append(clean)
        except (OSError, UnicodeDecodeError):
            continue

    # Read journal entries — contain bug fix patterns
    journal_index = brain_dir / "journal" / "index.json"
    if journal_index.exists():
        try:
            index = json.loads(journal_index.read_text(encoding="utf-8"))
            for entry in index:
                tags = entry.get("tags", [])
                title = entry.get("title", "")
                if tags or title:
                    directives.append(f"journal:{title}")
        except (json.JSONDecodeError, UnicodeDecodeError):
            pass

    return directives


def learn_from_project(project_path: str, quiet: bool = False) -> dict:
    """Scan project code and update team DNA."""
    active_team = get_active_team()
    if not active_team:
        if not quiet:
            print("❌ No active team.")
        return {}

    team_dir = get_team_dir(active_team)
    if not team_dir.exists():
        if not quiet:
            print(f"❌ Team '{active_team}' not found.")
        return {}

    # Scan code
    p = Path(project_path).resolve()
    if not p.exists():
        if not quiet:
            print(f"❌ Path not found: {p}")
        return {}

    result = scan_project(p)
    dna = encode_dna(result)

    # Update team DNA
    dna_file = team_dir / "hot" / "team.dna"
    old_dna = dna_file.read_text(encoding="utf-8").strip() if dna_file.exists() else ""

    if dna != old_dna:
        dna_file.write_text(dna, encoding="utf-8")
        # Also update project-level DNA
        project_dna = Path(project_path) / ".agent" / "brain" / "team_dna.txt"
        if project_dna.parent.exists():
            project_dna.write_text(dna, encoding="utf-8")
        if not quiet:
            print(f"🧬 DNA updated: {dna[:80]}")
        if old_dna:
            # Save old DNA to history
            history_dir = team_dir / "cold" / "history"
            history_dir.mkdir(parents=True, exist_ok=True)
            from datetime import datetime
            ts = datetime.now().strftime("%Y%m%d_%H%M%S")
            (history_dir / f"dna_{ts}.txt").write_text(old_dna, encoding="utf-8")
    else:
        if not quiet:
            print(f"🧬 DNA unchanged: {dna[:60]}")

    if quiet:
        print(f"TEAM_DNA={dna}")

    return result


def add_directive(directive: str, agent: str = "global", quiet: bool = False):
    """Add an observed directive as a rule. Dedup is handled by add_rule automatically."""
    active_team = get_active_team()
    if not active_team:
        if not quiet:
            print("❌ No active team.")
        return

    # add_rule handles dedup (Jaccard similarity check + frequency increment)
    add_rule(active_team, directive, agent)


def main():
    parser = argparse.ArgumentParser(description="Team Learner — extract habits from project + directives")
    parser.add_argument("--scan-project", default=None, help="Path to project to scan code style")
    parser.add_argument("--scan-artifacts", default=None, help="Path to .agent/brain/ to extract preferences")
    parser.add_argument("--directive", default=None, help="A specific observed directive to add as rule")
    parser.add_argument("--agent", default="global", help="Agent tag for directive")
    parser.add_argument("--quiet", action="store_true", help="Machine-readable output")
    args = parser.parse_args()

    if args.scan_project:
        learn_from_project(args.scan_project, args.quiet)

    if args.scan_artifacts:
        brain_path = Path(args.scan_artifacts)
        if brain_path.exists():
            directives = extract_from_artifacts(brain_path)
            freq = Counter(directives)
            for d, count in freq.most_common():
                if count >= 2:
                    add_directive(d, args.agent, args.quiet)

    if args.directive:
        add_directive(args.directive, args.agent, args.quiet)

    if not any([args.scan_project, args.scan_artifacts, args.directive]):
        # Default: scan current project
        learn_from_project(".", args.quiet)


if __name__ == "__main__":
    main()
