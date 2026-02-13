#!/usr/bin/env python3
import click
import os
import shutil
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
def init(ide):
    """Initialize VibeGravityKit in the current directory.
    
    Supported: all (default), antigravity, cursor, windsurf, cline
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

if __name__ == "__main__":
    main()
