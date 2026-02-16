#!/usr/bin/env python3
"""
Team Scanner — Scans existing projects to detect coding style, tech stack, and architecture patterns.
Zero dependencies (Python stdlib only).

Usage:
    python team_scanner.py --path ./my-project
    python team_scanner.py --path ./my-project --dna
    python team_scanner.py --path ./my-project --output team.json
"""

import argparse
import json
import os
import re
import sys
from collections import Counter
from pathlib import Path


# ── File extensions to scan ──────────────────────────────────────────
CODE_EXTENSIONS = {
    ".py", ".js", ".ts", ".jsx", ".tsx", ".java", ".cs", ".go",
    ".rb", ".php", ".rs", ".swift", ".kt", ".dart", ".vue", ".svelte",
}

IGNORE_DIRS = {
    "node_modules", ".git", "__pycache__", ".next", ".nuxt", "dist",
    "build", ".venv", "venv", "env", ".env", "vendor", ".agent",
    "coverage", ".cache", ".turbo",
}


# ── Stack Detection ──────────────────────────────────────────────────

def detect_stack(project_path: Path) -> dict:
    """Detect tech stack from config files."""
    stack = {
        "languages": [],
        "frontend": None,
        "backend": None,
        "database": None,
        "css": None,
        "testing": None,
        "bundler": None,
        "ci_cd": None,
        "containerized": False,
    }

    # Language detection by file count
    lang_counts = Counter()
    for root, dirs, files in os.walk(project_path):
        dirs[:] = [d for d in dirs if d not in IGNORE_DIRS]
        for f in files:
            ext = Path(f).suffix.lower()
            if ext == ".py": lang_counts["python"] += 1
            elif ext in (".js", ".jsx"): lang_counts["javascript"] += 1
            elif ext in (".ts", ".tsx"): lang_counts["typescript"] += 1
            elif ext == ".go": lang_counts["go"] += 1
            elif ext == ".rs": lang_counts["rust"] += 1
            elif ext == ".java": lang_counts["java"] += 1
            elif ext == ".cs": lang_counts["csharp"] += 1
            elif ext == ".rb": lang_counts["ruby"] += 1
            elif ext == ".php": lang_counts["php"] += 1
            elif ext == ".dart": lang_counts["dart"] += 1
            elif ext == ".swift": lang_counts["swift"] += 1
            elif ext == ".vue": lang_counts["vue"] += 1
            elif ext == ".svelte": lang_counts["svelte"] += 1

    stack["languages"] = [lang for lang, _ in lang_counts.most_common(3)]

    # package.json detection
    pkg_file = project_path / "package.json"
    if pkg_file.exists():
        try:
            pkg = json.loads(pkg_file.read_text(encoding="utf-8"))
            deps = {**pkg.get("dependencies", {}), **pkg.get("devDependencies", {})}

            # Frontend framework
            if "next" in deps: stack["frontend"] = "nextjs"
            elif "nuxt" in deps: stack["frontend"] = "nuxt"
            elif "vue" in deps: stack["frontend"] = "vue"
            elif "svelte" in deps: stack["frontend"] = "svelte"
            elif "react" in deps: stack["frontend"] = "react"

            # Bundler
            if "vite" in deps: stack["bundler"] = "vite"
            elif "webpack" in deps: stack["bundler"] = "webpack"
            elif "esbuild" in deps: stack["bundler"] = "esbuild"

            # Backend (Node)
            if "express" in deps: stack["backend"] = "express"
            elif "fastify" in deps: stack["backend"] = "fastify"
            elif "koa" in deps: stack["backend"] = "koa"
            elif "hono" in deps: stack["backend"] = "hono"

            # CSS
            if "tailwindcss" in deps: stack["css"] = "tailwind"
            elif "styled-components" in deps: stack["css"] = "styled-components"
            elif "sass" in deps or "node-sass" in deps: stack["css"] = "sass"

            # Testing
            if "vitest" in deps: stack["testing"] = "vitest"
            elif "jest" in deps: stack["testing"] = "jest"
            elif "mocha" in deps: stack["testing"] = "mocha"
            elif "playwright" in deps: stack["testing"] = "playwright"
            elif "cypress" in deps: stack["testing"] = "cypress"

            # Database
            if "prisma" in deps or "@prisma/client" in deps: stack["database"] = "prisma"
            elif "mongoose" in deps: stack["database"] = "mongodb"
            elif "pg" in deps: stack["database"] = "postgresql"
            elif "mysql2" in deps: stack["database"] = "mysql"
            elif "better-sqlite3" in deps: stack["database"] = "sqlite"
            elif "drizzle-orm" in deps: stack["database"] = "drizzle"
            elif "typeorm" in deps: stack["database"] = "typeorm"
        except (json.JSONDecodeError, UnicodeDecodeError):
            pass

    # Python detection
    for req_file in ["requirements.txt", "pyproject.toml", "Pipfile"]:
        req_path = project_path / req_file
        if req_path.exists():
            try:
                content = req_path.read_text(encoding="utf-8").lower()
                if "django" in content: stack["backend"] = "django"
                elif "fastapi" in content: stack["backend"] = "fastapi"
                elif "flask" in content: stack["backend"] = "flask"

                if "pytest" in content: stack["testing"] = "pytest"
                elif "unittest" in content: stack["testing"] = "unittest"

                if "sqlalchemy" in content: stack["database"] = "sqlalchemy"
                elif "psycopg" in content: stack["database"] = "postgresql"
                elif "pymongo" in content: stack["database"] = "mongodb"
            except UnicodeDecodeError:
                pass

    # TypeScript config
    if (project_path / "tsconfig.json").exists():
        try:
            ts_cfg = json.loads((project_path / "tsconfig.json").read_text(encoding="utf-8"))
            compiler = ts_cfg.get("compilerOptions", {})
            if compiler.get("strict"):
                if "typescript" not in stack["languages"]:
                    stack["languages"].insert(0, "typescript")
        except (json.JSONDecodeError, UnicodeDecodeError):
            pass

    # Docker
    if (project_path / "Dockerfile").exists() or (project_path / "docker-compose.yml").exists():
        stack["containerized"] = True

    # CI/CD
    if (project_path / ".github" / "workflows").exists(): stack["ci_cd"] = "github_actions"
    elif (project_path / ".gitlab-ci.yml").exists(): stack["ci_cd"] = "gitlab_ci"

    return stack


# ── Code Style Detection ─────────────────────────────────────────────

def detect_style(project_path: Path) -> dict:
    """Detect coding style by analyzing source files."""
    style = {
        "naming": "unknown",
        "comments": "unknown",
        "error_handling": "unknown",
        "quotes": "unknown",
        "semicolons": "unknown",
        "indent": "unknown",
        "function_length": "unknown",
    }

    naming_counts = Counter()  # camelCase vs snake_case
    quote_counts = Counter()   # single vs double
    semi_counts = Counter()    # with vs without
    indent_counts = Counter()  # 2 vs 4 vs tab
    total_lines = 0
    comment_lines = 0
    try_blocks = 0
    function_count = 0
    function_lengths = []
    current_func_lines = 0
    in_function = False

    for root, dirs, files in os.walk(project_path):
        dirs[:] = [d for d in dirs if d not in IGNORE_DIRS]
        for fname in files:
            ext = Path(fname).suffix.lower()
            if ext not in CODE_EXTENSIONS:
                continue

            fpath = Path(root) / fname
            try:
                lines = fpath.read_text(encoding="utf-8", errors="ignore").splitlines()
            except (OSError, UnicodeDecodeError):
                continue

            is_js = ext in (".js", ".jsx", ".ts", ".tsx", ".vue", ".svelte")
            is_py = ext == ".py"

            for line in lines:
                stripped = line.strip()
                total_lines += 1

                # Comments
                if stripped.startswith("//") or stripped.startswith("#") or stripped.startswith("/*") or stripped.startswith("*"):
                    comment_lines += 1

                # Naming: find function/variable declarations
                if is_js:
                    # JS/TS: function names, const/let names
                    for m in re.finditer(r'(?:function|const|let|var)\s+([a-zA-Z_]\w*)', stripped):
                        name = m.group(1)
                        if "_" in name and name != name.upper():
                            naming_counts["snake_case"] += 1
                        elif name[0].islower() and any(c.isupper() for c in name):
                            naming_counts["camelCase"] += 1
                        elif name[0].isupper():
                            naming_counts["PascalCase"] += 1
                elif is_py:
                    for m in re.finditer(r'(?:def|class)\s+([a-zA-Z_]\w*)', stripped):
                        name = m.group(1)
                        if "_" in name:
                            naming_counts["snake_case"] += 1
                        elif name[0].islower() and any(c.isupper() for c in name):
                            naming_counts["camelCase"] += 1
                        elif name[0].isupper():
                            naming_counts["PascalCase"] += 1

                # Quotes (JS/TS only)
                if is_js:
                    singles = len(re.findall(r"'[^']*'", stripped))
                    doubles = len(re.findall(r'"[^"]*"', stripped))
                    backticks = len(re.findall(r'`[^`]*`', stripped))
                    if singles > 0: quote_counts["single"] += singles
                    if doubles > 0: quote_counts["double"] += doubles

                # Semicolons (JS/TS only)
                if is_js and stripped and not stripped.startswith("//"):
                    if stripped.endswith(";"): semi_counts["yes"] += 1
                    elif stripped.endswith("{") or stripped.endswith("}") or stripped.endswith(","):
                        pass  # ignore structural lines
                    elif len(stripped) > 5: semi_counts["no"] += 1

                # Indentation
                if line and line[0] == " ":
                    spaces = len(line) - len(line.lstrip(" "))
                    if spaces == 2: indent_counts["2"] += 1
                    elif spaces == 4: indent_counts["4"] += 1
                elif line and line[0] == "\t":
                    indent_counts["tab"] += 1

                # Error handling
                if re.match(r'\s*(try|except|catch)\b', stripped):
                    try_blocks += 1

                # Function length tracking
                if re.match(r'\s*(def |function |const \w+ = |async function)', stripped):
                    if in_function and current_func_lines > 0:
                        function_lengths.append(current_func_lines)
                    in_function = True
                    current_func_lines = 0
                    function_count += 1
                elif in_function:
                    current_func_lines += 1

    if in_function and current_func_lines > 0:
        function_lengths.append(current_func_lines)

    # Analyze results
    if naming_counts:
        style["naming"] = naming_counts.most_common(1)[0][0]

    if total_lines > 0:
        ratio = comment_lines / total_lines
        if ratio < 0.03: style["comments"] = "minimal"
        elif ratio < 0.10: style["comments"] = "moderate"
        else: style["comments"] = "detailed"

    if function_count > 0:
        err_ratio = try_blocks / function_count
        if err_ratio < 0.1: style["error_handling"] = "minimal"
        elif err_ratio < 0.3: style["error_handling"] = "moderate"
        else: style["error_handling"] = "always"

    if quote_counts:
        style["quotes"] = quote_counts.most_common(1)[0][0]

    if semi_counts:
        winner = semi_counts.most_common(1)[0][0]
        style["semicolons"] = True if winner == "yes" else False

    if indent_counts:
        winner = indent_counts.most_common(1)[0][0]
        if winner == "tab": style["indent"] = "tabs"
        else: style["indent"] = f"{winner} spaces"

    if function_lengths:
        avg = sum(function_lengths) / len(function_lengths)
        if avg < 15: style["function_length"] = "short"
        elif avg < 30: style["function_length"] = "medium"
        else: style["function_length"] = "long"

    return style


# ── Architecture Detection ────────────────────────────────────────────

def detect_architecture(project_path: Path) -> dict:
    """Detect architecture patterns from folder structure."""
    arch = {"pattern": "unknown", "state_management": None, "api_style": None}

    # Check for common patterns
    src = project_path / "src"
    base = src if src.exists() else project_path

    feature_markers = {"features", "modules", "domains"}
    layer_markers = {"controllers", "services", "models", "repositories", "routes", "handlers"}

    found_feature = False
    found_layer = False

    for item in base.iterdir():
        if item.is_dir():
            name = item.name.lower()
            if name in feature_markers: found_feature = True
            if name in layer_markers: found_layer = True

    if found_feature: arch["pattern"] = "feature-based"
    elif found_layer: arch["pattern"] = "layer-based"
    else: arch["pattern"] = "flat"

    # State management detection (from package.json)
    pkg_file = project_path / "package.json"
    if pkg_file.exists():
        try:
            pkg = json.loads(pkg_file.read_text(encoding="utf-8"))
            deps = {**pkg.get("dependencies", {}), **pkg.get("devDependencies", {})}
            if "zustand" in deps: arch["state_management"] = "zustand"
            elif "redux" in deps or "@reduxjs/toolkit" in deps: arch["state_management"] = "redux"
            elif "jotai" in deps: arch["state_management"] = "jotai"
            elif "recoil" in deps: arch["state_management"] = "recoil"
            elif "pinia" in deps: arch["state_management"] = "pinia"
            elif "vuex" in deps: arch["state_management"] = "vuex"

            if "@tanstack/react-query" in deps: arch["api_style"] = "tanstack-query"
            elif "axios" in deps: arch["api_style"] = "axios"
            elif "swr" in deps: arch["api_style"] = "swr"
        except (json.JSONDecodeError, UnicodeDecodeError):
            pass

    return arch


# ── DNA Encoding ──────────────────────────────────────────────────────

def encode_dna(team_data: dict) -> str:
    """Encode team.json into compact 1-line DNA string."""
    parts = []
    stack = team_data.get("stack", {})
    style = team_data.get("code_style", {})
    arch = team_data.get("architecture", {})

    # Stack
    langs = stack.get("languages", [])
    if langs: parts.append(f"lang:{'+'.join(langs[:2])}")
    if stack.get("frontend"): parts.append(f"fe:{stack['frontend']}")
    if stack.get("backend"): parts.append(f"be:{stack['backend']}")
    if stack.get("database"): parts.append(f"db:{stack['database']}")
    if stack.get("css"): parts.append(f"css:{stack['css']}")
    if stack.get("bundler"): parts.append(f"bundler:{stack['bundler']}")
    if stack.get("testing"): parts.append(f"test:{stack['testing']}")

    # Style
    if style.get("naming") != "unknown": parts.append(f"naming:{style['naming']}")
    if style.get("comments") != "unknown": parts.append(f"comments:{style['comments']}")
    if style.get("errors", style.get("error_handling")) != "unknown":
        parts.append(f"errors:{style.get('errors', style.get('error_handling'))}")
    if style.get("indent") != "unknown": parts.append(f"indent:{style['indent']}")

    # Architecture
    if arch.get("pattern") != "unknown": parts.append(f"arch:{arch['pattern']}")
    if arch.get("state_management"): parts.append(f"state:{arch['state_management']}")

    return "|".join(parts)


def decode_dna(dna_string: str) -> dict:
    """Decode DNA string back into a dict."""
    result = {}
    for part in dna_string.split("|"):
        if ":" in part:
            key, value = part.split(":", 1)
            result[key] = value
    return result


# ── Main Scanner ──────────────────────────────────────────────────────

def scan_project(project_path: Path) -> dict:
    """Full project scan → team profile data."""
    return {
        "stack": detect_stack(project_path),
        "code_style": detect_style(project_path),
        "architecture": detect_architecture(project_path),
    }


def main():
    parser = argparse.ArgumentParser(description="Team Scanner — detect coding style from existing projects")
    parser.add_argument("--path", required=True, help="Path to project to scan")
    parser.add_argument("--output", help="Output file path (default: stdout)")
    parser.add_argument("--dna", action="store_true", help="Output compact DNA string only")
    parser.add_argument("--quiet", action="store_true", help="Machine-readable output")
    args = parser.parse_args()

    project_path = Path(args.path).resolve()
    if not project_path.exists():
        print(f"❌ Path not found: {project_path}")
        sys.exit(1)

    # Scan
    result = scan_project(project_path)
    dna = encode_dna(result)

    if args.dna:
        if args.quiet:
            print(f"TEAM_DNA={dna}")
        else:
            print(f"\n🧬 Team DNA:\n   {dna}\n")
        return

    if args.output:
        output_path = Path(args.output)
        output_path.write_text(json.dumps(result, indent=2, ensure_ascii=False), encoding="utf-8")
        if not args.quiet:
            print(f"✅ Saved to {output_path}")
            print(f"🧬 DNA: {dna}")
        return

    # Pretty print
    if args.quiet:
        print(json.dumps(result, ensure_ascii=False))
    else:
        print("\n📊 Team Scanner Results")
        print("=" * 50)

        s = result["stack"]
        print(f"\n🔧 Stack:")
        print(f"   Languages:  {', '.join(s['languages']) if s['languages'] else 'unknown'}")
        print(f"   Frontend:   {s['frontend'] or 'none'}")
        print(f"   Backend:    {s['backend'] or 'none'}")
        print(f"   Database:   {s['database'] or 'none'}")
        print(f"   CSS:        {s['css'] or 'none'}")
        print(f"   Testing:    {s['testing'] or 'none'}")
        print(f"   Bundler:    {s['bundler'] or 'none'}")
        print(f"   Docker:     {'yes' if s['containerized'] else 'no'}")
        print(f"   CI/CD:      {s['ci_cd'] or 'none'}")

        c = result["code_style"]
        print(f"\n✍️  Code Style:")
        print(f"   Naming:     {c['naming']}")
        print(f"   Comments:   {c['comments']}")
        print(f"   Errors:     {c['error_handling']}")
        print(f"   Quotes:     {c['quotes']}")
        print(f"   Semicolons: {c['semicolons']}")
        print(f"   Indent:     {c['indent']}")
        print(f"   Functions:  {c['function_length']}")

        a = result["architecture"]
        print(f"\n🏗️  Architecture:")
        print(f"   Pattern:    {a['pattern']}")
        print(f"   State:      {a['state_management'] or 'none'}")
        print(f"   API:        {a['api_style'] or 'none'}")

        print(f"\n🧬 Team DNA:")
        print(f"   {dna}\n")


if __name__ == "__main__":
    main()
