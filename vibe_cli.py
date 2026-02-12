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
    source_agent_dir = SOURCE_ROOT / ".agent"

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

if __name__ == "__main__":
    main()
