#!/usr/bin/env python3
"""
Team Manager — CRUD operations, inject, sync, rules, decay, and TF-IDF search for team profiles.
Stores teams globally at ~/.vibegravity/teams/.

Usage:
    python team_manager.py create <name> --scan <path>
    python team_manager.py list
    python team_manager.py show <name>
    python team_manager.py inject <name> <project_path>
    python team_manager.py rule add <rule> [--agent <agent>]
    python team_manager.py rule list
    python team_manager.py rule remove <id>
    python team_manager.py sync <source_team>
    python team_manager.py save-back <project_path>
    python team_manager.py export <name>
    python team_manager.py import <zip_path>
    python team_manager.py delete <name>
"""

import argparse
import json
import math
import os
import shutil
import sys
import zipfile
from collections import Counter
from datetime import datetime
from pathlib import Path

# Add scripts dir to path for team_scanner import
sys.path.insert(0, str(Path(__file__).parent))
from team_scanner import scan_project, encode_dna, decode_dna

TEAMS_DIR = Path.home() / ".vibegravity" / "teams"
ACTIVE_TEAM_FILE = Path.home() / ".vibegravity" / "active_team"


# ── Helpers ───────────────────────────────────────────────────────────

def get_team_dir(name: str) -> Path:
    return TEAMS_DIR / name


def ensure_team_structure(team_dir: Path):
    """Create the 3-tier directory structure."""
    (team_dir / "hot").mkdir(parents=True, exist_ok=True)
    (team_dir / "warm").mkdir(parents=True, exist_ok=True)
    (team_dir / "warm" / "journal" / "entries").mkdir(parents=True, exist_ok=True)
    (team_dir / "cold" / "archive").mkdir(parents=True, exist_ok=True)
    (team_dir / "cold" / "history").mkdir(parents=True, exist_ok=True)


def load_team_json(team_dir: Path) -> dict:
    team_file = team_dir / "team.json"
    if team_file.exists():
        return json.loads(team_file.read_text(encoding="utf-8"))
    return {}


def save_team_json(team_dir: Path, data: dict):
    (team_dir / "team.json").write_text(
        json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8"
    )


def get_active_team() -> str | None:
    if ACTIVE_TEAM_FILE.exists():
        return ACTIVE_TEAM_FILE.read_text(encoding="utf-8").strip()
    return None


def set_active_team(name: str):
    ACTIVE_TEAM_FILE.parent.mkdir(parents=True, exist_ok=True)
    ACTIVE_TEAM_FILE.write_text(name, encoding="utf-8")


# ── TF-IDF Search ────────────────────────────────────────────────────

def tokenize(text: str) -> list:
    """Simple tokenizer: lowercase, split on non-alpha."""
    import re
    return [w for w in re.split(r'\W+', text.lower()) if len(w) > 2]


def tfidf_search(query: str, documents: list[dict], key: str = "title") -> list[dict]:
    """Simple TF-IDF search over a list of dicts. Returns ranked results."""
    query_tokens = tokenize(query)
    if not query_tokens or not documents:
        return []

    # Build document frequency
    doc_freq = Counter()
    doc_tokens_list = []
    for doc in documents:
        text = doc.get(key, "") + " " + " ".join(doc.get("tags", []))
        tokens = tokenize(text)
        doc_tokens_list.append(tokens)
        for t in set(tokens):
            doc_freq[t] += 1

    n = len(documents)
    scored = []
    for i, (doc, doc_tokens) in enumerate(zip(documents, doc_tokens_list)):
        if not doc_tokens:
            continue
        score = 0.0
        tf_counter = Counter(doc_tokens)
        for qt in query_tokens:
            tf = tf_counter.get(qt, 0) / len(doc_tokens)
            idf = math.log((n + 1) / (doc_freq.get(qt, 0) + 1))
            score += tf * idf
        if score > 0:
            scored.append((score, i, doc))

    scored.sort(key=lambda x: -x[0])
    return [item[2] for item in scored[:10]]


# ── Create Team ───────────────────────────────────────────────────────

def create_team(name: str, scan_path: str = None):
    """Create a new team profile, optionally scanning a project."""
    team_dir = get_team_dir(name)
    if team_dir.exists():
        print(f"⚠️  Team '{name}' already exists. Use --force to overwrite.")
        return

    ensure_team_structure(team_dir)

    team_data = {
        "name": name,
        "created_at": datetime.now().isoformat(),
        "scanned_from": [],
        "stack": {},
        "code_style": {},
        "architecture": {},
    }

    # Scan if path provided
    if scan_path:
        project_path = Path(scan_path).resolve()
        if not project_path.exists():
            print(f"❌ Path not found: {project_path}")
            return
        print(f"🔍 Scanning {project_path}...")
        scan_result = scan_project(project_path)
        team_data["stack"] = scan_result["stack"]
        team_data["code_style"] = scan_result["code_style"]
        team_data["architecture"] = scan_result["architecture"]
        team_data["scanned_from"].append(str(project_path))

    # Save team.json
    save_team_json(team_dir, team_data)

    # Generate DNA
    dna = encode_dna(team_data)
    (team_dir / "hot" / "team.dna").write_text(dna, encoding="utf-8")

    # Init empty rules
    rules_data = {"global": [], "rules": []}
    (team_dir / "warm" / "rules.json").write_text(
        json.dumps(rules_data, indent=2), encoding="utf-8"
    )

    # Init empty journal index
    (team_dir / "warm" / "journal" / "index.json").write_text("[]", encoding="utf-8")

    # Empty top rules
    (team_dir / "hot" / "top_rules.md").write_text(
        "# Team Rules (auto-promoted, high frequency)\n\nNo rules yet.\n",
        encoding="utf-8"
    )

    # Set as active
    set_active_team(name)

    print(f"✅ Team '{name}' created!")
    if dna:
        print(f"🧬 DNA: {dna}")
    print(f"📁 Location: {team_dir}")


# ── Inject Team into Project ──────────────────────────────────────────

def inject_team(name: str, project_path: str):
    """Inject team profile into a project's .agent/brain/ directory."""
    team_dir = get_team_dir(name)
    if not team_dir.exists():
        print(f"❌ Team '{name}' not found.")
        return False

    brain_dir = Path(project_path) / ".agent" / "brain"
    brain_dir.mkdir(parents=True, exist_ok=True)

    team_data = load_team_json(team_dir)

    # 1. Copy DNA (Hot)
    dna_file = team_dir / "hot" / "team.dna"
    if dna_file.exists():
        dna = dna_file.read_text(encoding="utf-8").strip()
        # Smart filter: detect current project stack and filter DNA
        target_dna = dna  # TODO: filter based on project stack
        (brain_dir / "team_dna.txt").write_text(target_dna, encoding="utf-8")

    # 2. Copy top rules (Hot)
    top_rules = team_dir / "hot" / "top_rules.md"
    if top_rules.exists():
        (brain_dir / "team_rules.md").write_text(
            top_rules.read_text(encoding="utf-8"), encoding="utf-8"
        )

    # 3. Generate per-agent rules from warm/rules.json
    rules_file = team_dir / "warm" / "rules.json"
    if rules_file.exists():
        rules_data = json.loads(rules_file.read_text(encoding="utf-8"))
        rules_dir = brain_dir / "team_rules"
        rules_dir.mkdir(exist_ok=True)

        # Group rules by agent
        agent_rules = {}
        global_rules = rules_data.get("global", [])
        for rule in rules_data.get("rules", []):
            agent = rule.get("agent", "global")
            if agent not in agent_rules:
                agent_rules[agent] = list(global_rules)
            agent_rules[agent].append(rule.get("text", ""))

        # Write per-agent files
        for agent, rules in agent_rules.items():
            agent_file = rules_dir / f"{agent}.md"
            content = f"# Team Rules for {agent}\n\n"
            for r in rules:
                content += f"- {r}\n"
            agent_file.write_text(content, encoding="utf-8")

    # 4. Copy journal entries (Warm)
    journal_src = team_dir / "warm" / "journal"
    journal_dst = brain_dir / "journal"
    if journal_src.exists() and (journal_src / "index.json").exists():
        index = json.loads((journal_src / "index.json").read_text(encoding="utf-8"))
        if index:  # Only copy if there are entries
            journal_dst.mkdir(exist_ok=True)
            entries_dst = journal_dst / "entries"
            entries_dst.mkdir(exist_ok=True)

            # Copy index
            shutil.copy2(journal_src / "index.json", journal_dst / "index.json")

            # Copy entries
            entries_src = journal_src / "entries"
            if entries_src.exists():
                for entry_file in entries_src.iterdir():
                    if entry_file.is_file():
                        shutil.copy2(entry_file, entries_dst / entry_file.name)

    # 5. Write team metadata
    meta = {"team_name": name, "injected_at": datetime.now().isoformat()}
    (brain_dir / "team_meta.json").write_text(
        json.dumps(meta, indent=2), encoding="utf-8"
    )

    return True


# ── Save Journal Back to Team ─────────────────────────────────────────

def save_journal_back(name: str, project_path: str):
    """Sync new journal entries from project back to team."""
    team_dir = get_team_dir(name)
    if not team_dir.exists():
        print(f"❌ Team '{name}' not found.")
        return

    project_journal = Path(project_path) / ".agent" / "brain" / "journal"
    team_journal = team_dir / "warm" / "journal"

    if not project_journal.exists():
        print("ℹ️  No journal entries to sync.")
        return

    # Load team index
    team_index_file = team_journal / "index.json"
    team_index = json.loads(team_index_file.read_text(encoding="utf-8")) if team_index_file.exists() else []
    existing_titles = {e.get("title", "") for e in team_index}

    # Load project index
    proj_index_file = project_journal / "index.json"
    if not proj_index_file.exists():
        return

    proj_index = json.loads(proj_index_file.read_text(encoding="utf-8"))
    new_entries = 0

    for entry in proj_index:
        title = entry.get("title", "")

        # Dedup check: TF-IDF similarity
        if team_index:
            matches = tfidf_search(title, team_index, key="title")
            if matches:
                # Check if very similar entry exists
                top_match_title = matches[0].get("title", "")
                similarity = len(set(tokenize(title)) & set(tokenize(top_match_title))) / max(
                    len(set(tokenize(title))), 1
                )
                if similarity > 0.7:
                    # Duplicate — skip but increase frequency
                    for te in team_index:
                        if te.get("title") == top_match_title:
                            te["frequency"] = te.get("frequency", 1) + 1
                    continue

        # New entry — copy
        team_index.append(entry)
        entry_file = entry.get("file", "")
        if entry_file:
            src = project_journal / "entries" / entry_file
            dst = team_journal / "entries" / entry_file
            if src.exists():
                shutil.copy2(src, dst)
                new_entries += 1

    # Save updated index
    team_index_file.write_text(json.dumps(team_index, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"✅ Synced {new_entries} new journal entries to team '{name}'.")


# ── Rules Management ──────────────────────────────────────────────────

def add_rule(name: str, rule_text: str, agent: str = "global"):
    """Add a rule to the team."""
    team_dir = get_team_dir(name)
    if not team_dir.exists():
        print(f"❌ Team '{name}' not found.")
        return

    rules_file = team_dir / "warm" / "rules.json"
    rules_data = json.loads(rules_file.read_text(encoding="utf-8")) if rules_file.exists() else {"global": [], "rules": []}

    rule_entry = {
        "id": len(rules_data.get("rules", [])) + 1,
        "text": rule_text,
        "agent": agent,
        "frequency": 1,
        "created_at": datetime.now().isoformat(),
        "last_used": datetime.now().isoformat(),
    }

    if agent == "global":
        rules_data["global"].append(rule_text)
    rules_data.setdefault("rules", []).append(rule_entry)

    rules_file.write_text(json.dumps(rules_data, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"✅ Rule added to team '{name}' (agent: {agent})")


def list_rules(name: str):
    """List all rules in a team."""
    team_dir = get_team_dir(name)
    rules_file = team_dir / "warm" / "rules.json"
    if not rules_file.exists():
        print("No rules found.")
        return

    rules_data = json.loads(rules_file.read_text(encoding="utf-8"))
    print(f"\n📋 Rules for team '{name}':")
    for rule in rules_data.get("rules", []):
        agent_tag = f"[{rule['agent']}]" if rule['agent'] != 'global' else "[global]"
        freq = rule.get("frequency", 0)
        print(f"  #{rule['id']} {agent_tag} {rule['text']} (freq: {freq})")
    print()


def remove_rule(name: str, rule_id: int):
    """Remove a rule by ID."""
    team_dir = get_team_dir(name)
    rules_file = team_dir / "warm" / "rules.json"
    if not rules_file.exists():
        return

    rules_data = json.loads(rules_file.read_text(encoding="utf-8"))
    rules_data["rules"] = [r for r in rules_data.get("rules", []) if r["id"] != rule_id]
    rules_data["global"] = [r["text"] for r in rules_data["rules"] if r["agent"] == "global"]
    rules_file.write_text(json.dumps(rules_data, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"✅ Rule #{rule_id} removed.")


def promote_hot_rules(name: str, min_frequency: int = 3):
    """Promote high-frequency rules to Hot tier."""
    team_dir = get_team_dir(name)
    rules_file = team_dir / "warm" / "rules.json"
    if not rules_file.exists():
        return

    rules_data = json.loads(rules_file.read_text(encoding="utf-8"))
    hot_rules = [r for r in rules_data.get("rules", []) if r.get("frequency", 0) >= min_frequency]

    if hot_rules:
        content = "# Team Rules (high frequency — auto-promoted)\n\n"
        for r in sorted(hot_rules, key=lambda x: -x.get("frequency", 0)):
            content += f"- {r['text']}\n"
        (team_dir / "hot" / "top_rules.md").write_text(content, encoding="utf-8")


# ── Sync Teams ────────────────────────────────────────────────────────

def sync_teams(target_name: str, source_name: str):
    """Merge source team's knowledge into target team."""
    source_dir = get_team_dir(source_name)
    target_dir = get_team_dir(target_name)

    if not source_dir.exists():
        print(f"❌ Source team '{source_name}' not found.")
        return
    if not target_dir.exists():
        print(f"❌ Target team '{target_name}' not found.")
        return

    # Merge rules
    src_rules_file = source_dir / "warm" / "rules.json"
    tgt_rules_file = target_dir / "warm" / "rules.json"

    if src_rules_file.exists():
        src_rules = json.loads(src_rules_file.read_text(encoding="utf-8"))
        tgt_rules = json.loads(tgt_rules_file.read_text(encoding="utf-8")) if tgt_rules_file.exists() else {"global": [], "rules": []}

        existing = {r["text"] for r in tgt_rules.get("rules", [])}
        new_count = 0
        for rule in src_rules.get("rules", []):
            if rule["text"] not in existing:
                rule["id"] = len(tgt_rules["rules"]) + 1
                tgt_rules["rules"].append(rule)
                if rule["agent"] == "global":
                    tgt_rules["global"].append(rule["text"])
                new_count += 1

        tgt_rules_file.write_text(json.dumps(tgt_rules, indent=2, ensure_ascii=False), encoding="utf-8")
        print(f"  📋 Merged {new_count} new rules.")

    # Merge journal
    src_journal = source_dir / "warm" / "journal"
    tgt_journal = target_dir / "warm" / "journal"

    if (src_journal / "index.json").exists():
        src_index = json.loads((src_journal / "index.json").read_text(encoding="utf-8"))
        tgt_index = json.loads((tgt_journal / "index.json").read_text(encoding="utf-8")) if (tgt_journal / "index.json").exists() else []

        existing_titles = {e.get("title", "") for e in tgt_index}
        new_entries = 0
        for entry in src_index:
            if entry.get("title", "") not in existing_titles:
                tgt_index.append(entry)
                # Copy entry file
                entry_file = entry.get("file", "")
                if entry_file:
                    src_file = src_journal / "entries" / entry_file
                    dst_file = tgt_journal / "entries" / entry_file
                    if src_file.exists():
                        shutil.copy2(src_file, dst_file)
                        new_entries += 1

        (tgt_journal / "index.json").write_text(json.dumps(tgt_index, indent=2, ensure_ascii=False), encoding="utf-8")
        print(f"  📚 Merged {new_entries} journal entries.")

    print(f"✅ Synced '{source_name}' → '{target_name}'")


# ── Export / Import ───────────────────────────────────────────────────

def export_team(name: str):
    """Export team as .zip file."""
    team_dir = get_team_dir(name)
    if not team_dir.exists():
        print(f"❌ Team '{name}' not found.")
        return

    zip_path = Path.cwd() / f"team-{name}.zip"
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
        for root, dirs, files in os.walk(team_dir):
            for f in files:
                fpath = Path(root) / f
                arcname = fpath.relative_to(team_dir.parent)
                zf.write(fpath, arcname)

    print(f"✅ Exported to {zip_path}")


def import_team(zip_path: str):
    """Import team from .zip file."""
    zp = Path(zip_path)
    if not zp.exists():
        print(f"❌ File not found: {zp}")
        return

    with zipfile.ZipFile(zp, "r") as zf:
        zf.extractall(TEAMS_DIR)

    print(f"✅ Imported team from {zp}")


# ── List / Show / Delete ─────────────────────────────────────────────

def list_teams():
    """List all available teams."""
    if not TEAMS_DIR.exists():
        print("No teams found. Create one with: vibegravity team create <name> --scan <path>")
        return

    active = get_active_team()
    teams = [d.name for d in TEAMS_DIR.iterdir() if d.is_dir()]
    if not teams:
        print("No teams found.")
        return

    print("\n🏠 Teams:")
    for t in sorted(teams):
        team_dir = TEAMS_DIR / t
        dna_file = team_dir / "hot" / "team.dna"
        dna = dna_file.read_text(encoding="utf-8").strip() if dna_file.exists() else "no DNA"
        marker = " ← active" if t == active else ""
        print(f"  {'→' if t == active else ' '} {t}{marker}")
        print(f"    🧬 {dna[:80]}{'...' if len(dna) > 80 else ''}")
    print()


def show_team(name: str):
    """Show detailed team info."""
    team_dir = get_team_dir(name)
    if not team_dir.exists():
        print(f"❌ Team '{name}' not found.")
        return

    data = load_team_json(team_dir)
    dna_file = team_dir / "hot" / "team.dna"
    dna = dna_file.read_text(encoding="utf-8").strip() if dna_file.exists() else "none"

    # Count entries
    journal_index = team_dir / "warm" / "journal" / "index.json"
    j_count = len(json.loads(journal_index.read_text(encoding="utf-8"))) if journal_index.exists() else 0

    rules_file = team_dir / "warm" / "rules.json"
    r_count = len(json.loads(rules_file.read_text(encoding="utf-8")).get("rules", [])) if rules_file.exists() else 0

    print(f"\n📋 Team: {name}")
    print(f"   Created:  {data.get('created_at', 'unknown')}")
    print(f"   Scanned:  {', '.join(data.get('scanned_from', [])) or 'none'}")
    print(f"   Rules:    {r_count}")
    print(f"   Journal:  {j_count} entries")
    print(f"   🧬 DNA:   {dna}")
    print()


def delete_team(name: str):
    """Delete a team."""
    team_dir = get_team_dir(name)
    if not team_dir.exists():
        print(f"❌ Team '{name}' not found.")
        return

    shutil.rmtree(team_dir)
    if get_active_team() == name:
        ACTIVE_TEAM_FILE.unlink(missing_ok=True)
    print(f"✅ Team '{name}' deleted.")


# ── CLI ───────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="Team Manager — manage persistent team profiles")
    sub = parser.add_subparsers(dest="command")

    # create
    p_create = sub.add_parser("create", help="Create a new team")
    p_create.add_argument("name", help="Team name")
    p_create.add_argument("--scan", help="Path to project to scan")

    # list
    sub.add_parser("list", help="List all teams")

    # show
    p_show = sub.add_parser("show", help="Show team details")
    p_show.add_argument("name", help="Team name")

    # delete
    p_del = sub.add_parser("delete", help="Delete a team")
    p_del.add_argument("name", help="Team name")

    # inject
    p_inject = sub.add_parser("inject", help="Inject team into project")
    p_inject.add_argument("name", help="Team name")
    p_inject.add_argument("--project", default=".", help="Project path")

    # save-back
    p_save = sub.add_parser("save-back", help="Sync journal back to team")
    p_save.add_argument("name", help="Team name")
    p_save.add_argument("--project", default=".", help="Project path")

    # rule
    p_rule = sub.add_parser("rule", help="Manage rules")
    rule_sub = p_rule.add_subparsers(dest="rule_action")
    p_rule_add = rule_sub.add_parser("add", help="Add a rule")
    p_rule_add.add_argument("rule_text", help="Rule text")
    p_rule_add.add_argument("--agent", default="global", help="Agent tag")
    rule_sub.add_parser("list", help="List rules")
    p_rule_rm = rule_sub.add_parser("remove", help="Remove a rule")
    p_rule_rm.add_argument("rule_id", type=int, help="Rule ID")

    # sync
    p_sync = sub.add_parser("sync", help="Merge another team's knowledge")
    p_sync.add_argument("source", help="Source team name to merge from")

    # export
    p_export = sub.add_parser("export", help="Export team as zip")
    p_export.add_argument("name", help="Team name")

    # import
    p_import = sub.add_parser("import", help="Import team from zip")
    p_import.add_argument("zip_path", help="Path to zip file")

    args = parser.parse_args()
    active = get_active_team()

    if args.command == "create":
        create_team(args.name, args.scan)
    elif args.command == "list":
        list_teams()
    elif args.command == "show":
        show_team(args.name)
    elif args.command == "delete":
        delete_team(args.name)
    elif args.command == "inject":
        if inject_team(args.name, args.project):
            print(f"✅ Team '{args.name}' injected into {args.project}")
    elif args.command == "save-back":
        save_journal_back(args.name, args.project)
    elif args.command == "rule":
        name = active or ""
        if not name:
            print("❌ No active team. Set one with: vibegravity team create <name>")
            return
        if args.rule_action == "add":
            add_rule(name, args.rule_text, args.agent)
        elif args.rule_action == "list":
            list_rules(name)
        elif args.rule_action == "remove":
            remove_rule(name, args.rule_id)
    elif args.command == "sync":
        if not active:
            print("❌ No active team to sync into.")
            return
        sync_teams(active, args.source)
    elif args.command == "export":
        export_team(args.name)
    elif args.command == "import":
        import_team(args.zip_path)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
