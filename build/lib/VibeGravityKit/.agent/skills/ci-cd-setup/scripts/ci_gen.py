#!/usr/bin/env python3
"""
CI/CD Setup — Generate GitHub Actions.

Usage:
    python ci_gen.py --platform github --type node
"""

import argparse

TEMPLATES = {
    "node": """name: Node.js CI

on:
  push:
    branches: [ "main" ]
  pull_request:
    branches: [ "main" ]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v3
    - name: Use Node.js
      uses: actions/setup-node@v3
      with:
        node-version: '18.x'
        cache: 'npm'
    - run: npm ci
    - run: npm run build --if-present
    - run: npm test""",
    
    "python": """name: Python CI

on:
  push:
    branches: [ "main" ]
  pull_request:
    branches: [ "main" ]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v3
    - name: Set up Python
      uses: actions/setup-python@v3
      with:
        python-version: "3.9"
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install flake8 pytest
        if [ -f requirements.txt ]; then pip install -r requirements.txt; fi
    - name: Lint with flake8
      run: flake8 .
    - name: Test with pytest
      run: pytest"""
}

def generate(type):
    print(f"🚀 Generating GitHub Actions for {type}...")
    print("\n📄 .github/workflows/main.yml:")
    print(TEMPLATES.get(type, TEMPLATES["node"]))

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--platform", default="github")
    parser.add_argument("--type", choices=["node", "python"], required=True)
    args = parser.parse_args()
    generate(args.type)

if __name__ == "__main__":
    main()
