#!/usr/bin/env python3
"""
Project Scaffolder — Generate commands and files to bootstrap a project.

Usage:
    python scaffold.py --stack "nextjs-supabase" --name "my-app" --path "./my-app"
"""

import argparse
import json
import sys

# === Templates per stack ===
SCAFFOLDS = {
    "nextjs-supabase": {
        "display_name": "Next.js + Supabase",
        "init_commands": [
            'npx -y create-next-app@latest "{path}" --typescript --tailwind --eslint --app --src-dir --import-alias "@/*" --use-npm',
            'cd "{path}" && npm install @supabase/supabase-js @supabase/auth-helpers-nextjs'
        ],
        "extra_packages": {
            "ui": "npm install lucide-react clsx",
            "forms": "npm install react-hook-form zod @hookform/resolvers",
            "state": "npm install zustand"
        },
        "directories": [
            "src/components/ui",
            "src/components/layout",
            "src/components/features",
            "src/lib",
            "src/hooks",
            "src/services",
            "src/styles",
            "src/types",
            "public/images",
            "public/fonts"
        ],
        "files": {
            "src/lib/supabase.ts": "// Supabase client initialization\nimport { createClient } from '@supabase/supabase-js';\n\nconst supabaseUrl = process.env.NEXT_PUBLIC_SUPABASE_URL!;\nconst supabaseKey = process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!;\n\nexport const supabase = createClient(supabaseUrl, supabaseKey);",
            "src/lib/utils.ts": "// Utility functions\nimport { clsx, type ClassValue } from 'clsx';\n\nexport function cn(...inputs: ClassValue[]) {\n  return clsx(inputs);\n}",
            "src/lib/constants.ts": "// Application constants\nexport const APP_NAME = '{name}';\nexport const APP_DESCRIPTION = '';\nexport const APP_URL = process.env.NEXT_PUBLIC_APP_URL || 'http://localhost:3000';",
            "src/types/index.ts": "// Global type definitions\nexport type {}; // placeholder",
            ".env.example": "# Supabase\nNEXT_PUBLIC_SUPABASE_URL=\nNEXT_PUBLIC_SUPABASE_ANON_KEY=\nSUPABASE_SERVICE_ROLE_KEY=\n\n# App\nNEXT_PUBLIC_APP_URL=http://localhost:3000\nNEXTAUTH_SECRET=\n\n# External APIs\n",
            ".prettierrc": '{\n  "semi": true,\n  "singleQuote": true,\n  "tabWidth": 2,\n  "trailingComma": "es5",\n  "printWidth": 100\n}'
        }
    },
    "vite-react": {
        "display_name": "Vite + React",
        "init_commands": [
            'npm create -y vite@latest "{path}" -- --template react',
            'cd "{path}" && npm install'
        ],
        "extra_packages": {
            "routing": "npm install react-router-dom",
            "ui": "npm install lucide-react clsx",
            "state": "npm install zustand",
            "forms": "npm install react-hook-form zod @hookform/resolvers"
        },
        "directories": [
            "src/components/ui",
            "src/components/layout",
            "src/components/features",
            "src/pages",
            "src/hooks",
            "src/services",
            "src/utils",
            "src/styles",
            "public/images"
        ],
        "files": {
            "src/utils/helpers.js": "// Utility helper functions\nexport function cn(...classes) {\n  return classes.filter(Boolean).join(' ');\n}",
            "src/styles/variables.css": "/* Design tokens */\n:root {\n  --color-primary: #6366f1;\n  --color-secondary: #8b5cf6;\n  --color-bg: #0f172a;\n  --color-surface: #1e293b;\n  --color-text: #f8fafc;\n  --color-muted: #94a3b8;\n  --font-sans: 'Inter', system-ui, sans-serif;\n  --radius: 8px;\n}",
            ".env.example": "# API\nVITE_API_URL=http://localhost:3001\nVITE_APP_NAME={name}\n",
            ".prettierrc": '{\n  "semi": true,\n  "singleQuote": true,\n  "tabWidth": 2\n}'
        }
    },
    "python-fastapi": {
        "display_name": "Python FastAPI",
        "init_commands": [
            'mkdir -p "{path}"',
            'cd "{path}" && python -m venv .venv',
            'cd "{path}" && pip install fastapi uvicorn sqlalchemy psycopg2-binary python-dotenv pydantic-settings'
        ],
        "extra_packages": {
            "auth": "pip install python-jose passlib[bcrypt]",
            "cors": "# CORS built into FastAPI",
            "testing": "pip install pytest httpx"
        },
        "directories": [
            "app/models",
            "app/schemas",
            "app/routes",
            "app/services",
            "app/middleware",
            "app/utils",
            "tests"
        ],
        "files": {
            "app/__init__.py": "",
            "app/main.py": "from fastapi import FastAPI\nfrom fastapi.middleware.cors import CORSMiddleware\n\napp = FastAPI(title='{name}', version='0.1.0')\n\napp.add_middleware(\n    CORSMiddleware,\n    allow_origins=['*'],\n    allow_credentials=True,\n    allow_methods=['*'],\n    allow_headers=['*'],\n)\n\n@app.get('/')\ndef root():\n    return {'message': '{name} API is running'}",
            "app/config.py": "from pydantic_settings import BaseSettings\n\nclass Settings(BaseSettings):\n    database_url: str = 'sqlite:///./dev.db'\n    secret_key: str = 'change-me'\n    class Config:\n        env_file = '.env'\n\nsettings = Settings()",
            "app/models/__init__.py": "",
            "app/schemas/__init__.py": "",
            "app/routes/__init__.py": "",
            "app/services/__init__.py": "",
            "app/utils/__init__.py": "",
            "tests/__init__.py": "",
            "requirements.txt": "fastapi\nuvicorn\nsqlalchemy\npsycopg2-binary\npython-dotenv\npydantic-settings",
            ".env.example": "# Database\nDATABASE_URL=postgresql://user:pass@localhost:5432/{name}\n\n# Auth\nSECRET_KEY=change-me-to-random-string\n\n# App\nDEBUG=true",
            ".gitignore": "__pycache__/\n*.py[cod]\n.venv/\n.env\n*.db\n.pytest_cache/"
        }
    },
    "html-css-js": {
        "display_name": "HTML + CSS + Vanilla JS",
        "init_commands": [
            'mkdir -p "{path}"'
        ],
        "extra_packages": {},
        "directories": [
            "css",
            "js",
            "images",
            "fonts"
        ],
        "files": {
            "index.html": '<!DOCTYPE html>\n<html lang="en">\n<head>\n  <meta charset="UTF-8">\n  <meta name="viewport" content="width=device-width, initial-scale=1.0">\n  <meta name="description" content="">\n  <title>{name}</title>\n  <link rel="stylesheet" href="css/style.css">\n</head>\n<body>\n  <header id="header"></header>\n  <main id="main"></main>\n  <footer id="footer"></footer>\n  <script src="js/app.js"></script>\n</body>\n</html>',
            "css/style.css": "/* Design tokens */\n:root {\n  --color-primary: #6366f1;\n  --color-bg: #0f172a;\n  --color-text: #f8fafc;\n  --font-sans: 'Inter', system-ui, sans-serif;\n}\n\n/* Reset */\n*, *::before, *::after {\n  box-sizing: border-box;\n  margin: 0;\n  padding: 0;\n}\n\nbody {\n  font-family: var(--font-sans);\n  background: var(--color-bg);\n  color: var(--color-text);\n  line-height: 1.6;\n}",
            "js/app.js": "// {name} — Main application\n'use strict';\n\ndocument.addEventListener('DOMContentLoaded', () => {\n  console.log('{name} loaded');\n});",
            ".gitignore": ".DS_Store\nThumbs.db\n*.log"
        }
    }
}


def parse_args():
    parser = argparse.ArgumentParser(description="Project Scaffolder")
    parser.add_argument("--stack", type=str, required=True, help="Stack ID: nextjs-supabase, vite-react, python-fastapi, html-css-js")
    parser.add_argument("--name", type=str, required=True, help="Project Name")
    parser.add_argument("--path", type=str, required=True, help="Target path to create project")
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    return parser.parse_args()


def generate_scaffold(stack_id, project_name, target_path):
    """Generate scaffold instructions."""
    if stack_id not in SCAFFOLDS:
        available = ", ".join(SCAFFOLDS.keys())
        return {"error": f"Invalid stack '{stack_id}'. Available stacks: {available}"}

    template = SCAFFOLDS[stack_id]
    result = {
        "stack": template["display_name"],
        "project_name": project_name,
        "path": target_path,
        "steps": []
    }

    # Step 1: Init commands
    result["steps"].append({
        "step": 1,
        "title": "Initialize Project",
        "commands": [cmd.format(path=target_path, name=project_name) for cmd in template["init_commands"]]
    })

    # Step 2: Extra packages
    if template["extra_packages"]:
        result["steps"].append({
            "step": 2,
            "title": "Install Extra Packages (Optional)",
            "packages": {k: cmd.format(path=target_path) for k, cmd in template["extra_packages"].items()}
        })

    # Step 3: Create directories
    result["steps"].append({
        "step": 3,
        "title": "Create Directories",
        "directories": template["directories"]
    })

    # Step 4: Create files
    files = {}
    for filepath, content in template["files"].items():
        files[filepath] = content.replace("{name}", project_name).replace("{path}", target_path)

    result["steps"].append({
        "step": 4,
        "title": "Create Configuration Files",
        "files": files
    })

    # Step 5: Git init
    result["steps"].append({
        "step": 5,
        "title": "Init Git",
        "commands": [
            f'cd "{target_path}" && git init',
            f'cd "{target_path}" && git add .',
            f'cd "{target_path}" && git commit -m "feat: initial project setup — {template["display_name"]}"'
        ]
    })

    return result


def print_readable(result):
    """Print results in a readable format."""
    if "error" in result:
        print(f"❌ Error: {result['error']}")
        return

    print("=" * 60)
    print(f"📦 PROJECT SCAFFOLD: {result['project_name']}")
    print(f"🛠️  Stack: {result['stack']}")
    print(f"📁 Path: {result['path']}")
    print("=" * 60)

    for step in result["steps"]:
        print(f"\n{'─' * 60}")
        print(f"  Step {step['step']}: {step['title']}")
        print(f"{'─' * 60}")

        if "commands" in step:
            for cmd in step["commands"]:
                print(f"  $ {cmd}")

        if "packages" in step:
            for pkg_name, cmd in step["packages"].items():
                print(f"  [{pkg_name}] $ {cmd}")

        if "directories" in step:
            for d in step["directories"]:
                print(f"  📁 {d}/")

        if "files" in step:
            for f in step["files"]:
                print(f"  📄 {f}")

    print(f"\n{'=' * 60}")
    print("✅ Scaffold ready! Run the commands above in order.")


if __name__ == "__main__":
    args = parse_args()
    result = generate_scaffold(args.stack, args.name, args.path)

    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print_readable(result)
