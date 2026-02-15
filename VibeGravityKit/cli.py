#!/usr/bin/env python3
import click
import json
import os
import shutil
import sys
from pathlib import Path

# Get the absolute path to the VibeGravityKit source directory
# This assumes vibe_cli.py is in the root of the repo
SOURCE_ROOT = Path(__file__).resolve().parent

@click.group()
def main():
    """VibeGravityKit CLI - Manage your AI Agent Team."""
    pass

@main.command()
@click.argument('ide', default='all', required=False)
@click.option('--team', default=None, help='Team profile to inject (from ~/.vibegravity/teams/)')
def init(ide, team):
    """Initialize VibeGravityKit in the current directory.
    
    Supported: all (default), antigravity, cursor, windsurf, cline
    Use --team to inject a persistent team profile.
    """
    package_dir = Path(__file__).resolve().parent
    
    # IDE configuration mapping
    ide_config = {
        "antigravity": {
            "source": package_dir / ".agent",
            "target": Path.cwd() / ".agent",
            "label": ".agent/ (workflows + skills)",
        },
        "cursor": {
            "source": package_dir / "ide-adapters" / "cursor",
            "target": Path.cwd() / ".cursor" / "rules",
            "label": ".cursor/rules/ (Cursor IDE)",
        },
        "windsurf": {
            "source": package_dir / "ide-adapters" / "windsurf",
            "target": Path.cwd() / ".windsurf" / "rules",
            "label": ".windsurf/rules/ (Windsurf IDE)",
        },
        "cline": {
            "source": package_dir / "ide-adapters" / "cline",
            "target": Path.cwd() / ".clinerules",
            "label": ".clinerules/ (Cline IDE)",
        },
    }
    
    # Determine which IDEs to install
    if ide == "all":
        targets = list(ide_config.keys())
        click.echo("🚀 Installing VibeGravityKit for ALL IDEs...")
    elif ide in ide_config:
        targets = [ide]
        click.echo(f"🚀 Installing VibeGravityKit for {ide}...")
    else:
        click.echo(f"❌ Unknown IDE: '{ide}'")
        click.echo(f"   Supported: all, {', '.join(ide_config.keys())}")
        return
    
    installed = 0
    for target_ide in targets:
        config = ide_config[target_ide]
        source_dir = config["source"]
        target_dir = config["target"]
        
        if not source_dir.exists():
            click.echo(f"  ⚠️  Skipped {target_ide}: source not found")
            continue
        
        try:
            if target_dir.exists():
                shutil.rmtree(target_dir)
            target_dir.parent.mkdir(parents=True, exist_ok=True)
            shutil.copytree(source_dir, target_dir)
            click.echo(f"  ✅ {config['label']}")
            installed += 1
        except Exception as e:
            click.echo(f"  ❌ {target_ide}: {str(e)}")
    
    click.echo(f"\n✨ Done! Installed for {installed} IDE(s).")

    # Inject team profile if specified
    if team:
        scripts_dir = package_dir / ".agent" / "skills" / "team-manager" / "scripts"
        sys.path.insert(0, str(scripts_dir))
        try:
            from team_manager import inject_team, get_team_dir
            team_dir = get_team_dir(team)
            if not team_dir.exists():
                click.echo(f"\n⚠️  Team '{team}' not found. Skipping team injection.")
                click.echo(f"   Create one: vibegravity team create {team} --scan ./your-project")
            else:
                if inject_team(team, str(Path.cwd())):
                    click.echo(f"\n🧬 Team '{team}' injected!")
                    dna_file = team_dir / "hot" / "team.dna"
                    if dna_file.exists():
                        click.echo(f"   DNA: {dna_file.read_text(encoding='utf-8').strip()[:80]}")
        except ImportError:
            click.echo(f"\n⚠️  team-manager skill not found. Team injection skipped.")
        finally:
            if str(scripts_dir) in sys.path:
                sys.path.remove(str(scripts_dir))
    else:
        click.echo("\n💡 Tip: Use --team <name> to inject your coding style and knowledge.")

    click.echo("👉 Use @[/planner], @[/architect], etc. in your AI chat.")

@main.command()
def list():
    """List available AI Agents and their roles."""
    # .agent is inside vibecore package
    workflows_dir = Path(__file__).resolve().parent / ".agent" / "workflows"
    if not workflows_dir.exists():
        click.echo("❌ .agent/workflows directory not found.")
        return

    click.echo("\n🤖 Available VibeGravityKit Agents:\n")
    click.echo(f"{'Agent':<25} {'Role Description':<50}")
    click.echo("-" * 75)

    for workflow_file in sorted(workflows_dir.glob("*.md")):
        name = workflow_file.stem
        description = "No description available."
        try:
            with open(workflow_file, "r", encoding="utf-8") as f:
                content = f.read()
                if "description:" in content:
                    # Simple parsing of frontmatter description
                    import re
                    match = re.search(r"description:\s*(.+)", content)
                    if match:
                        description = match.group(1).strip()
        except Exception:
            pass
        
        click.echo(f"@[/{name:<22}] {description}")
    click.echo("")

@main.command()
def doctor():
    """Check environment health (Python, Node, Git)."""
    import subprocess
    import shutil

    click.echo("\n🩺 VibeGravityKit Doctor - Checking Environment...\n")
    
    checks = [
        ("python", "--version", "Python"),
        ("node", "--version", "Node.js"),
        ("git", "--version", "Git"),
        ("npm", "--version", "npm"),
    ]

    all_good = True

    for cmd, arg, name in checks:
        if shutil.which(cmd):
            try:
                result = subprocess.run([cmd, arg], capture_output=True, text=True, check=True)
                version = result.stdout.strip().split('\n')[0]
                click.echo(f"✅ {name:<10}: Found ({version})")
            except Exception:
                click.echo(f"⚠️  {name:<10}: Found but failed to run")
                all_good = False
        else:
            click.echo(f"❌ {name:<10}: NOT FOUND")
            all_good = False

    # Check .agent folder
    if (Path.cwd() / ".agent").exists():
        click.echo(f"✅ .agent    : Found in current directory")
    else:
        click.echo(f"⚠️  .agent    : Not found (Run 'vibe init' to install)")

    click.echo("")
    if all_good:
        click.echo("🎉 Your environment is healthy and ready to vibe!")
    else:
        click.echo("🩹 Some tools are missing. Please install them to use full capabilities.")

@main.command()
def update():
    """Update VibeGravityKit to the latest version from GitHub."""
    import subprocess
    
    click.echo("⬇️  Checking for updates from GitHub...")
    try:
        # Check if we are in a git repo
        # If installed as package, __file__ is inside vibecore/cli.py
        # Git root should be 2 levels up: vibecore -> repo root
        git_root = Path(__file__).resolve().parent.parent
        
        if not (git_root / ".git").exists():
             click.echo("⚠️  Not a git repository. Attempting update via Pip...")
             subprocess.run([
                 "pip", "install", "--upgrade", 
                 "git+https://github.com/Nhqvu2005/VibeGravityKit.git"
             ], check=True)
             click.echo("✅ Updated to latest version via Pip.")
             return

        # Fetch and pull
        subprocess.run(["git", "fetch"], cwd=git_root, check=True)
        status = subprocess.run(["git", "status", "-uno"], cwd=git_root, capture_output=True, text=True)
        
        if "behind" in status.stdout:
            click.echo("🚀 New version available! Updating...")
            subprocess.run(["git", "pull"], cwd=git_root, check=True)
            click.echo("✅ Updated to latest version.")
            
            # Show new version
            version_file = Path(__file__).resolve().parent / "VERSION"
            if version_file.exists():
                with open(version_file, "r") as f:
                    click.echo(f"📦 Current Version: {f.read().strip()}")
        else:
            click.echo("✨ You are already on the latest version.")
            
    except Exception as e:
        click.echo(f"❌ Update failed: {str(e)}")

@main.command()
def version():
    """Show current VibeGravityKit version."""
    version_file = Path(__file__).resolve().parent / "VERSION"
    if version_file.exists():
        with open(version_file, "r") as f:
            click.echo(f"v{f.read().strip()}")
    else:
        click.echo("Version info not found.")

@main.command(context_settings=dict(ignore_unknown_options=True, allow_extra_args=True))
@click.pass_context
def brain(ctx):
    """Manage project brain — context, decisions, conventions."""
    import subprocess as sp
    script = Path(__file__).resolve().parent / ".agent" / "skills" / "brain-manager" / "scripts" / "brain.py"
    if not script.exists():
        click.echo("❌ brain-manager skill not found. Run 'vibegravity init' first.")
        return
    sp.run(["python", str(script)] + ctx.args)

@main.command(context_settings=dict(ignore_unknown_options=True, allow_extra_args=True))
@click.pass_context
def journal(ctx):
    """Knowledge journal — capture lessons, bugs, insights."""
    import subprocess as sp
    script = Path(__file__).resolve().parent / ".agent" / "skills" / "journal-manager" / "scripts" / "journal.py"
    if not script.exists():
        click.echo("❌ journal-manager skill not found. Run 'vibegravity init' first.")
        return
    sp.run(["python", str(script)] + ctx.args)

@main.group(context_settings=dict(ignore_unknown_options=True, allow_extra_args=True))
@click.pass_context
def team(ctx):
    """Manage persistent team profiles — style, rules, and knowledge."""
    pass

@team.command("create")
@click.argument('name')
def team_create(name):
    """Create a new empty team profile (learns as you work)."""
    import subprocess as sp
    script = Path(__file__).resolve().parent / ".agent" / "skills" / "team-manager" / "scripts" / "team_manager.py"
    if not script.exists():
        click.echo("❌ team-manager skill not found.")
        return
    sp.run(["python", str(script), "create", name])

@team.command("scan")
@click.argument('name')
@click.option('--path', required=True, help='Path to project to scan')
def team_scan(name, path):
    """Manually scan a project to learn coding style (optional — agents auto-scan)."""
    import subprocess as sp
    scanner = Path(__file__).resolve().parent / ".agent" / "skills" / "team-manager" / "scripts" / "team_scanner.py"
    manager = Path(__file__).resolve().parent / ".agent" / "skills" / "team-manager" / "scripts" / "team_manager.py"
    if not scanner.exists():
        click.echo("❌ team-manager skill not found.")
        return
    click.echo(f"🔍 Scanning {path}...")
    # Scan and output
    sp.run(["python", str(scanner), "--path", path])
    # Update team with scan data
    sp.run(["python", str(scanner), "--path", path, "--output",
            str(Path.home() / ".vibegravity" / "teams" / name / "team.json")])
    # Regenerate DNA
    result = sp.run(["python", str(scanner), "--path", path, "--dna", "--quiet"],
                    capture_output=True, text=True)
    dna_line = result.stdout.strip().replace("TEAM_DNA=", "")
    if dna_line:
        dna_file = Path.home() / ".vibegravity" / "teams" / name / "hot" / "team.dna"
        dna_file.parent.mkdir(parents=True, exist_ok=True)
        dna_file.write_text(dna_line, encoding="utf-8")
        click.echo(f"🧬 DNA updated: {dna_line[:80]}")

@team.command("learn")
@click.option('--conversations', default=None, help='Path to conversation logs dir')
def team_learn(conversations):
    """Scan conversation logs to extract coding habits and preferences.
    
    Runs automatically by leader/quickstart at plan confirmation.
    Can also be run manually to learn from past conversations.
    """
    import subprocess as sp
    script = Path(__file__).resolve().parent / ".agent" / "skills" / "team-manager" / "scripts" / "team_learner.py"
    if not script.exists():
        click.echo("❌ team-learner script not found.")
        return
    cmd = ["python", str(script)]
    if conversations:
        cmd.extend(["--conversations", conversations])
    sp.run(cmd)

@team.command("list")
def team_list():
    """List all team profiles."""
    import subprocess as sp
    script = Path(__file__).resolve().parent / ".agent" / "skills" / "team-manager" / "scripts" / "team_manager.py"
    if not script.exists():
        click.echo("❌ team-manager skill not found.")
        return
    sp.run(["python", str(script), "list"])

@team.command("show")
@click.argument('name')
def team_show(name):
    """Show team profile details."""
    import subprocess as sp
    script = Path(__file__).resolve().parent / ".agent" / "skills" / "team-manager" / "scripts" / "team_manager.py"
    if not script.exists():
        click.echo("❌ team-manager skill not found.")
        return
    sp.run(["python", str(script), "show", name])

@team.command("delete")
@click.argument('name')
def team_delete(name):
    """Delete a team profile."""
    import subprocess as sp
    script = Path(__file__).resolve().parent / ".agent" / "skills" / "team-manager" / "scripts" / "team_manager.py"
    if not script.exists():
        click.echo("❌ team-manager skill not found.")
        return
    sp.run(["python", str(script), "delete", name])

@team.command("sync")
@click.argument('source')
def team_sync(source):
    """Merge another team's knowledge into active team."""
    import subprocess as sp
    script = Path(__file__).resolve().parent / ".agent" / "skills" / "team-manager" / "scripts" / "team_manager.py"
    if not script.exists():
        click.echo("❌ team-manager skill not found.")
        return
    sp.run(["python", str(script), "sync", source])

@team.command("export")
@click.argument('name')
def team_export(name):
    """Export team profile as zip file."""
    import subprocess as sp
    script = Path(__file__).resolve().parent / ".agent" / "skills" / "team-manager" / "scripts" / "team_manager.py"
    if not script.exists():
        click.echo("❌ team-manager skill not found.")
        return
    sp.run(["python", str(script), "export", name])

@team.command("import")
@click.argument('zip_path')
def team_import(zip_path):
    """Import team profile from zip file."""
    import subprocess as sp
    script = Path(__file__).resolve().parent / ".agent" / "skills" / "team-manager" / "scripts" / "team_manager.py"
    if not script.exists():
        click.echo("❌ team-manager skill not found.")
        return
    sp.run(["python", str(script), "import", zip_path])

@team.group("rule")
def team_rule():
    """Manage team rules."""
    pass

@team_rule.command("add")
@click.argument('rule_text')
@click.option('--agent', default='global', help='Target agent (default: global)')
def rule_add(rule_text, agent):
    """Add a rule to the active team."""
    import subprocess as sp
    script = Path(__file__).resolve().parent / ".agent" / "skills" / "team-manager" / "scripts" / "team_manager.py"
    if not script.exists():
        click.echo("❌ team-manager skill not found.")
        return
    cmd = ["python", str(script), "rule", "add", rule_text, "--agent", agent]
    sp.run(cmd)

@team_rule.command("list")
def rule_list():
    """List all rules in active team."""
    import subprocess as sp
    script = Path(__file__).resolve().parent / ".agent" / "skills" / "team-manager" / "scripts" / "team_manager.py"
    if not script.exists():
        click.echo("❌ team-manager skill not found.")
        return
    sp.run(["python", str(script), "rule", "list"])

@team_rule.command("remove")
@click.argument('rule_id', type=int)
def rule_remove(rule_id):
    """Remove a rule by ID."""
    import subprocess as sp
    script = Path(__file__).resolve().parent / ".agent" / "skills" / "team-manager" / "scripts" / "team_manager.py"
    if not script.exists():
        click.echo("❌ team-manager skill not found.")
        return
    sp.run(["python", str(script), "rule", "remove", str(rule_id)])


if __name__ == "__main__":
    main()
