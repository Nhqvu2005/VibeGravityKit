#!/usr/bin/env python3
"""
README Generator v2 — Auto-scan project, generate concise & stunning README.

Usage:
    python readme_gen.py --path .
    python readme_gen.py --path . --style minimal
    python readme_gen.py --path . --style standard --name "My Project" --author "user"
"""

import argparse, json, os, re, sys

# ─── Project Scanner ──────────────────────────────────────────────

def scan_project(path):
    """Auto-detect project metadata from files."""
    ctx = {
        "name": os.path.basename(os.path.abspath(path)),
        "version": None, "license": "MIT", "slogan": None,
        "author": None, "repo_url": None, "image": None,
        "tech": set(), "has_docker": False, "has_agent": False,
        "scripts": {}, "features": [], "install_cmd": None,
        "skill_count": 0, "workflow_count": 0,
    }

    # package.json (Node/JS)
    pkg = _read_json(path, "package.json")
    if pkg:
        ctx["name"] = pkg.get("name", ctx["name"])
        ctx["version"] = pkg.get("version", ctx["version"])
        ctx["license"] = pkg.get("license", ctx["license"])
        ctx["slogan"] = pkg.get("description")
        ctx["author"] = pkg.get("author") if isinstance(pkg.get("author"), str) else None
        repo = pkg.get("repository", {})
        if isinstance(repo, dict): ctx["repo_url"] = repo.get("url", "").replace("git+", "").replace(".git", "")
        ctx["scripts"] = pkg.get("scripts", {})
        ctx["install_cmd"] = "npm install"
        ctx["tech"].add("node")
        deps = {**pkg.get("dependencies", {}), **pkg.get("devDependencies", {})}
        if "typescript" in deps or "ts-node" in deps: ctx["tech"].add("typescript")
        if "react" in deps: ctx["tech"].add("react")
        if "next" in deps: ctx["tech"].add("nextjs")
        if "vue" in deps: ctx["tech"].add("vue")
        if "express" in deps: ctx["tech"].add("node")
        if "tailwindcss" in deps: ctx["tech"].add("tailwind")

    # setup.py / pyproject.toml (Python)
    if os.path.exists(os.path.join(path, "setup.py")) or os.path.exists(os.path.join(path, "pyproject.toml")):
        ctx["tech"].add("python")
        ctx["install_cmd"] = ctx["install_cmd"] or "pip install ."

    if os.path.exists(os.path.join(path, "requirements.txt")):
        ctx["tech"].add("python")
        ctx["install_cmd"] = ctx["install_cmd"] or "pip install -r requirements.txt"

    # VERSION file
    ver_file = os.path.join(path, "VERSION")
    if os.path.exists(ver_file):
        ctx["version"] = open(ver_file).read().strip()

    # LICENSE detection
    lic_file = os.path.join(path, "LICENSE")
    if os.path.exists(lic_file):
        lic_text = open(lic_file).read(500).lower()
        if "apache" in lic_text: ctx["license"] = "Apache-2.0"
        elif "gpl" in lic_text: ctx["license"] = "GPL-3.0"
        elif "mit" in lic_text: ctx["license"] = "MIT"

    # Docker
    if os.path.exists(os.path.join(path, "Dockerfile")) or os.path.exists(os.path.join(path, "docker-compose.yml")):
        ctx["has_docker"] = True
        ctx["tech"].add("docker")

    # TypeScript
    if os.path.exists(os.path.join(path, "tsconfig.json")):
        ctx["tech"].add("typescript")

    # .agent/ skills & workflows
    agent_dir = os.path.join(path, ".agent")
    if os.path.isdir(agent_dir):
        ctx["has_agent"] = True
        skills_dir = os.path.join(agent_dir, "skills")
        wf_dir = os.path.join(agent_dir, "workflows")
        if os.path.isdir(skills_dir):
            ctx["skill_count"] = len([d for d in os.listdir(skills_dir) if os.path.isdir(os.path.join(skills_dir, d))])
        if os.path.isdir(wf_dir):
            ctx["workflow_count"] = len([f for f in os.listdir(wf_dir) if f.endswith(".md")])

    return ctx


def _read_json(base, filename):
    fp = os.path.join(base, filename)
    if os.path.exists(fp):
        try:
            return json.load(open(fp, encoding="utf-8"))
        except: pass
    return None

# ─── Badge Generator ─────────────────────────────────────────────

def generate_badges(ctx, templates):
    badges = []
    badge_map = templates.get("badge_map", {})
    dynamic = templates.get("dynamic_badges", {})

    # Version badge
    if ctx["version"]:
        b = dynamic.get("version", "").format(version=ctx["version"], repo_url=ctx.get("repo_url", "#"))
        if b: badges.append(b)

    # Tech badges
    for tech in sorted(ctx["tech"]):
        if tech in badge_map:
            badges.append(badge_map[tech])

    # License badge
    lic_key = ctx["license"].lower().split("-")[0]
    if lic_key in badge_map:
        badges.append(badge_map[lic_key])
    else:
        badges.append(badge_map.get("mit", ""))

    # GitHub stars (if repo_url available)
    if ctx.get("repo_url") and "github.com" in (ctx["repo_url"] or ""):
        parts = ctx["repo_url"].rstrip("/").split("/")
        if len(parts) >= 2:
            owner, repo = parts[-2], parts[-1]
            star_badge = dynamic.get("stars", "").format(owner=owner, repo=repo, repo_url=ctx["repo_url"])
            if star_badge: badges.append(star_badge)

    return badges

# ─── README Builder ───────────────────────────────────────────────

def build_readme(ctx, style, templates, overrides):
    # Apply overrides
    if overrides.get("name"): ctx["name"] = overrides["name"]
    if overrides.get("slogan"): ctx["slogan"] = overrides["slogan"]
    if overrides.get("author"): ctx["author"] = overrides["author"]
    if overrides.get("image"): ctx["image"] = overrides["image"]
    if overrides.get("repo_url"): ctx["repo_url"] = overrides["repo_url"]

    sections = templates.get("section_order", {}).get(style, ["hero", "features", "install", "license"])
    badges = generate_badges(ctx, templates)

    lines = []

    for section in sections:
        if section == "hero":
            lines.extend(_build_hero(ctx, badges))
        elif section == "features":
            lines.extend(_build_features(ctx))
        elif section == "install":
            lines.extend(_build_install(ctx))
        elif section == "usage":
            lines.extend(_build_usage(ctx))
        elif section == "cli":
            if ctx["scripts"] or ctx.get("has_agent"):
                lines.extend(_build_cli(ctx))
        elif section == "config":
            lines.extend(_build_config_placeholder())
        elif section == "structure":
            lines.extend(_build_structure(ctx))
        elif section == "tech_stack":
            if len(ctx["tech"]) > 1:
                lines.extend(_build_tech_stack(ctx))
        elif section == "contributing":
            lines.extend(_build_contributing())
        elif section == "changelog":
            lines.extend(_build_changelog())
        elif section == "license":
            lines.extend(_build_license(ctx))

    return "\n".join(lines)


def _build_hero(ctx, badges):
    lines = ['<div align="center">', '']
    lines.append(f'# {ctx["name"]}')
    lines.append('')

    # Badges — row of 6 max, then <br>
    row1, row2 = badges[:6], badges[6:]
    if row1:
        lines.append(" ".join(row1))
    if row2:
        lines.append("<br>")
        lines.append(" ".join(row2))
    lines.append('')

    # Image
    if ctx.get("image"):
        lines.append(f'<img src="{ctx["image"]}" alt="{ctx["name"]}" width="100%">')
        lines.append('')

    # Tagline
    slogan = ctx.get("slogan") or f'A {"/".join(sorted(ctx["tech"]))} project.'
    lines.append(f'**{slogan}**')
    lines.append('')
    lines.append('</div>')
    lines.append('')
    lines.append('---')
    lines.append('')
    return lines


def _build_features(ctx):
    lines = ['## ✨ Features', '']
    lines.append('| Feature | Description |')
    lines.append('| :--- | :--- |')

    if ctx.get("features"):
        for f in ctx["features"]:
            lines.append(f'| {f["icon"]} **{f["name"]}** | {f["desc"]} |')
    else:
        # Placeholder features based on detected tech
        placeholders = [
            ("⚡", "Fast Setup", "Get running in under a minute"),
            ("🛡️", "Production Ready", "Built with best practices"),
            ("📦", "Zero Config", "Sensible defaults, customize when needed"),
        ]
        if ctx.get("has_docker"):
            placeholders.append(("🐳", "Docker Support", "One-command containerized deployment"))
        if ctx.get("has_agent"):
            placeholders.append(("🤖", f'{ctx["skill_count"]} AI Skills', f'{ctx["workflow_count"]} agent workflows included'))

        for icon, name, desc in placeholders:
            lines.append(f'| {icon} **{name}** | {desc} |')

    lines.extend(['', '---', ''])
    return lines


def _build_install(ctx):
    lines = ['## 🚀 Quick Start', '', '```bash']

    repo_name = ctx["name"].lower().replace(" ", "-")
    repo_url = ctx.get("repo_url") or f"https://github.com/USERNAME/{repo_name}"

    lines.append(f'git clone {repo_url}.git')
    lines.append(f'cd {repo_name}')
    if ctx.get("install_cmd"):
        lines.append(ctx["install_cmd"])

    # Start command
    if "dev" in ctx.get("scripts", {}):
        lines.append("npm run dev")
    elif "start" in ctx.get("scripts", {}):
        lines.append("npm start")

    lines.extend(['```', ''])

    # Prerequisites one-liner
    prereqs = []
    if "python" in ctx["tech"]: prereqs.append("Python 3.9+")
    if "node" in ctx["tech"]: prereqs.append("Node.js 18+")
    if prereqs:
        lines.append(f'> Requires: {" · ".join(prereqs)}')
        lines.append('')

    lines.extend(['---', ''])
    return lines


def _build_usage(ctx):
    lines = ['## 📖 Usage', '']
    if "python" in ctx["tech"]:
        lines.extend([
            '```python',
            f'import {ctx["name"].lower().replace("-", "_").replace(" ", "_")}',
            '',
            '# Your code here',
            '```',
        ])
    elif "node" in ctx["tech"]:
        lines.extend([
            '```javascript',
            f'const app = require("{ctx["name"]}");',
            '',
            '// Your code here',
            '```',
        ])
    else:
        lines.append('<!-- Add usage examples here -->')

    lines.extend(['', '---', ''])
    return lines


def _build_cli(ctx):
    lines = ['## 🛠️ CLI Commands', '']
    lines.append('| Command | Description |')
    lines.append('| :--- | :--- |')

    if ctx.get("scripts"):
        for cmd, script in list(ctx["scripts"].items())[:10]:
            lines.append(f'| `npm run {cmd}` | `{script}` |')

    lines.extend(['', '---', ''])
    return lines


def _build_config_placeholder():
    return [
        '## ⚙️ Configuration', '',
        '| Variable | Description | Default |',
        '| :--- | :--- | :--- |',
        '| `PORT` | Server port | `3000` |',
        '| `NODE_ENV` | Environment | `development` |',
        '', '---', '',
    ]


def _build_structure(ctx):
    lines = ['## 📂 Project Structure', '', '```']
    tree = [
        f'{ctx["name"]}/',
        '├── src/           # Source code',
        '├── tests/         # Test files',
    ]
    if ctx.get("has_docker"):
        tree.append('├── Dockerfile     # Container config')
    if ctx.get("has_agent"):
        tree.append('├── .agent/        # AI agent workflows & skills')
    tree.append('└── README.md')
    lines.extend(tree)
    lines.extend(['```', '', '---', ''])
    return lines


def _build_tech_stack(ctx):
    lines = ['## 🧰 Tech Stack', '']
    lines.append('| Technology | Purpose |')
    lines.append('| :--- | :--- |')

    tech_labels = {
        "python": ("Python", "Core language"),
        "node": ("Node.js", "Runtime"),
        "typescript": ("TypeScript", "Type safety"),
        "react": ("React", "UI framework"),
        "nextjs": ("Next.js", "Full-stack framework"),
        "vue": ("Vue.js", "UI framework"),
        "docker": ("Docker", "Containerization"),
        "tailwind": ("Tailwind CSS", "Styling"),
    }
    for tech in sorted(ctx["tech"]):
        if tech in tech_labels:
            name, purpose = tech_labels[tech]
            lines.append(f'| **{name}** | {purpose} |')

    lines.extend(['', '---', ''])
    return lines


def _build_contributing():
    return [
        '## 🤝 Contributing', '',
        '1. Fork → `git checkout -b feature/amazing` → Commit → PR', '',
        '---', '',
    ]


def _build_changelog():
    return [
        '## 📋 Changelog', '',
        'See [CHANGELOG.md](CHANGELOG.md) for full history.', '',
        '---', '',
    ]


def _build_license(ctx):
    author = ctx.get("author") or "Your Name"
    lic = ctx.get("license", "MIT")
    return [f'{lic} © [{author}](https://github.com/{author})', '']


# ─── Main ─────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="README Generator v2")
    parser.add_argument("--path", default=".", help="Project root to scan")
    parser.add_argument("--style", default="standard", choices=["minimal", "standard", "detailed"])
    parser.add_argument("--name", default=None, help="Override project name")
    parser.add_argument("--slogan", default=None, help="Override tagline")
    parser.add_argument("--author", default=None, help="Override author")
    parser.add_argument("--image", default=None, help="Hero image URL")
    parser.add_argument("--repo-url", default=None, help="Repository URL")
    parser.add_argument("--output", default=None, help="Output file (default: stdout)")
    args = parser.parse_args()

    # Load templates
    tpl_path = os.path.join(os.path.dirname(__file__), "..", "data", "readme_templates.json")
    templates = {}
    if os.path.exists(tpl_path):
        templates = json.load(open(tpl_path, encoding="utf-8"))

    # Scan project
    ctx = scan_project(args.path)

    # Build README
    overrides = {
        "name": args.name, "slogan": args.slogan,
        "author": args.author, "image": args.image,
        "repo_url": args.repo_url,
    }
    readme = build_readme(ctx, args.style, templates, overrides)

    # Output
    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(readme)
        print(f"✅ README written to {args.output}", file=sys.stderr)
    else:
        print(readme)


if __name__ == "__main__":
    main()
