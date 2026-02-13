#!/usr/bin/env python3
"""
journal.py — 2-tier knowledge journal for development insights.
Tier 1: index.json (quick lookup)
Tier 2: entries/*.md (full content)
"""

import json
import argparse
import re
from pathlib import Path
from datetime import datetime

JOURNAL_DIR = Path.cwd() / ".agent" / "brain" / "journal"
INDEX_FILE = JOURNAL_DIR / "index.json"
ENTRIES_DIR = JOURNAL_DIR / "entries"


def ensure_journal():
    """Ensure journal directory structure exists."""
    JOURNAL_DIR.mkdir(parents=True, exist_ok=True)
    ENTRIES_DIR.mkdir(parents=True, exist_ok=True)

    if not INDEX_FILE.exists():
        INDEX_FILE.write_text(json.dumps({"entries": []}, indent=2), encoding='utf-8')


def load_index():
    """Load the journal index."""
    ensure_journal()
    return json.loads(INDEX_FILE.read_text(encoding='utf-8'))


def save_index(index):
    """Save the journal index."""
    INDEX_FILE.write_text(json.dumps(index, indent=2, ensure_ascii=False), encoding='utf-8')


def slugify(text):
    """Convert text to filename-safe slug."""
    slug = text.lower().strip()
    slug = re.sub(r'[^a-z0-9\s-]', '', slug)
    slug = re.sub(r'[\s]+', '-', slug)
    return slug[:50]


def cmd_add(args):
    """Add a new journal entry."""
    index = load_index()

    now = datetime.now()
    date_str = now.strftime("%Y-%m-%d")
    entry_id = f"{date_str}_{slugify(args.title)}"
    tags = [t.strip() for t in args.tags.split(',')] if args.tags else []

    # Create index entry (Tier 1)
    index_entry = {
        "id": entry_id,
        "title": args.title,
        "tags": tags,
        "date": date_str,
        "category": args.category or "general",
    }
    index["entries"].append(index_entry)
    save_index(index)

    # Create markdown entry (Tier 2)
    body = args.body or "(No details provided)"
    entry_content = f"""# {args.title}

**Date:** {date_str}
**Tags:** {', '.join(tags) if tags else 'none'}
**Category:** {args.category or 'general'}

---

{body}
"""

    entry_file = ENTRIES_DIR / f"{entry_id}.md"
    entry_file.write_text(entry_content, encoding='utf-8')

    print(f"✅ Journal entry added: {args.title}")
    print(f"   ID: {entry_id}")
    print(f"   File: {entry_file}")


def cmd_list(args):
    """List recent journal entries."""
    index = load_index()
    entries = index.get("entries", [])

    if not entries:
        print("📓 Journal is empty. Add entries with: journal.py add --title '...'")
        return

    limit = args.limit or 10
    print(f"📓 Journal ({len(entries)} entries, showing last {min(limit, len(entries))}):\n")

    for entry in entries[-limit:]:
        tags = ', '.join(entry.get('tags', []))
        tag_str = f" [{tags}]" if tags else ""
        print(f"  [{entry['date']}] {entry['title']}{tag_str}")
        print(f"             ID: {entry['id']}")


def cmd_search(args):
    """Search entries by keyword or tag."""
    index = load_index()
    query = args.query.lower()

    matches = []
    for entry in index.get("entries", []):
        title_match = query in entry.get("title", "").lower()
        tag_match = query in [t.lower() for t in entry.get("tags", [])]
        cat_match = query in entry.get("category", "").lower()

        if title_match or tag_match or cat_match:
            matches.append(entry)

    if not matches:
        print(f"🔍 No entries found for '{args.query}'")
        return

    print(f"🔍 Found {len(matches)} entries for '{args.query}':\n")
    for entry in matches:
        tags = ', '.join(entry.get('tags', []))
        print(f"  [{entry['date']}] {entry['title']} [{tags}]")
        print(f"             ID: {entry['id']}")


def cmd_show(args):
    """Show full content of a journal entry."""
    entry_file = ENTRIES_DIR / f"{args.id}.md"

    if not entry_file.exists():
        # Try partial match
        matching = list(ENTRIES_DIR.glob(f"*{args.id}*.md"))
        if matching:
            entry_file = matching[0]
        else:
            print(f"❌ Entry not found: {args.id}")
            return

    print(entry_file.read_text(encoding='utf-8'))


def main():
    parser = argparse.ArgumentParser(description='VibeGravityKit Knowledge Journal')
    subparsers = parser.add_subparsers(dest='command')

    # add
    add_cmd = subparsers.add_parser('add', help='Add a journal entry')
    add_cmd.add_argument('--title', '-t', required=True, help='Entry title')
    add_cmd.add_argument('--body', '-b', help='Entry body/details')
    add_cmd.add_argument('--tags', help='Comma-separated tags')
    add_cmd.add_argument('--category', '-c', help='Category (e.g., bug-fix, decision, insight)')

    # list
    list_cmd = subparsers.add_parser('list', help='List recent entries')
    list_cmd.add_argument('--limit', '-n', type=int, default=10)

    # search
    search_cmd = subparsers.add_parser('search', help='Search entries')
    search_cmd.add_argument('query', help='Search keyword')

    # show
    show_cmd = subparsers.add_parser('show', help='Show entry details')
    show_cmd.add_argument('id', help='Entry ID (or partial match)')

    args = parser.parse_args()

    commands = {
        'add': cmd_add,
        'list': cmd_list,
        'search': cmd_search,
        'show': cmd_show,
    }

    if args.command in commands:
        commands[args.command](args)
    else:
        parser.print_help()


if __name__ == '__main__':
    main()
