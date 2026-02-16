#!/usr/bin/env python3
"""
Note Taker - Knowledge Guide Skill
Appends structured notes to .agent/memory/ideas_inbox.md
"""

import argparse
import datetime
from pathlib import Path

MEMORY_DIR = Path(__file__).resolve().parent.parent.parent.parent / "memory"
INBOX_FILE = MEMORY_DIR / "ideas_inbox.md"

def ensure_inbox_exists():
    if not MEMORY_DIR.exists():
        MEMORY_DIR.mkdir(parents=True, exist_ok=True)
    if not INBOX_FILE.exists():
        with open(INBOX_FILE, "w", encoding="utf-8") as f:
            f.write("# Ideas Inbox\n\nCaptured ideas and improvements from Knowledge Guide sessions.\n\n---\n\n")

def add_note(title, content, tags):
    ensure_inbox_exists()
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    tag_list = " ".join([f"#{t.strip()}" for t in tags.split(",") if t.strip()])
    
    entry = f"""
## [{timestamp}] {title}
**Tags:** {tag_list}
**Status:** New

{content}

---
"""
    with open(INBOX_FILE, "a", encoding="utf-8") as f:
        f.write(entry)
    
    print(f"✅ Note added to {INBOX_FILE}")

def main():
    parser = argparse.ArgumentParser(description="Add note to ideas inbox")
    parser.add_argument("--title", required=True, help="Title of the idea")
    parser.add_argument("--content", required=True, help="Detailed content of the idea")
    parser.add_argument("--tags", default="", help="Comma-separated tags (e.g. backend,optimization)")
    
    args = parser.parse_args()
    add_note(args.title, args.content, args.tags)

if __name__ == "__main__":
    main()
