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
@click.argument('ide', default='antigravity', required=False)
def init(ide):
    """Initialize VibeGravityKit in the current directory."""
    target_dir = Path.cwd() / ".agent"
    
    # When installed as a package, .agent is inside VibeGravityKit module
    source_agent_dir = Path(__file__).resolve().parent / ".agent"

    if target_dir.exists():
        click.echo("⚠️  .agent directory already exists here!")
        if not click.confirm("Do you want to overwrite it?"):
            return

    click.echo(f"🚀 Initializing VibeGravityKit for {ide}...")
    
    try:
        # Copy the .agent folder
        if source_agent_dir.exists():
            if target_dir.exists():
                shutil.rmtree(target_dir)
            shutil.copytree(source_agent_dir, target_dir)
            click.echo("✅ Copied .agent/ workflows and skills.")
        else:
            click.echo(f"❌ Error: Could not find source .agent folder at {source_agent_dir}")
            return

        click.echo("\n✨ VibeGravityKit installed successfully!")
        click.echo("👉 You can now mention @[/planner], @[/architect], etc. in your AI chat.")
        
    except Exception as e:
        click.echo(f"❌ Installation failed: {str(e)}")

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
             click.echo("⚠️  This installation is not a git repository. Cannot auto-update.")
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

if __name__ == "__main__":
    main()
