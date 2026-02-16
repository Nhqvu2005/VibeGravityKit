#!/usr/bin/env python3
"""
string_extractor.py — Extract hardcoded strings from source code
for internationalization (i18n).
"""

import os
import re
import json
import argparse
from pathlib import Path
from collections import defaultdict

# Patterns for hardcoded strings in different languages
EXTRACTION_PATTERNS = {
    '.jsx': [
        # JSX text content: <p>Hello World</p>
        re.compile(r'>\s*([A-Z][^<>{}\n]{2,})\s*<', re.MULTILINE),
        # JSX attributes with strings: title="Hello"
        re.compile(r'(?:title|placeholder|label|alt|aria-label)=\s*"([^"]{2,})"'),
    ],
    '.tsx': [
        re.compile(r'>\s*([A-Z][^<>{}\n]{2,})\s*<', re.MULTILINE),
        re.compile(r'(?:title|placeholder|label|alt|aria-label)=\s*"([^"]{2,})"'),
    ],
    '.vue': [
        # Vue template text
        re.compile(r'>\s*([A-Z][^<>{}\n]{2,})\s*<', re.MULTILINE),
        re.compile(r'(?:placeholder|label|title)=\s*"([^"]{2,})"'),
    ],
    '.py': [
        # Python strings in common user-facing patterns
        re.compile(r'(?:message|label|title|text|description)\s*=\s*["\']([^"\']{3,})["\']'),
        re.compile(r'click\.echo\s*\(\s*f?["\']([^"\']{3,})["\']'),
    ],
    '.html': [
        re.compile(r'>\s*([A-Z][^<>{}\n]{2,})\s*<', re.MULTILINE),
        re.compile(r'(?:placeholder|title|alt)=\s*"([^"]{2,})"'),
    ],
}

SKIP_DIRS = {'node_modules', '.git', '__pycache__', '.next', 'dist', 'venv', 'locales', 'i18n'}

# Words to skip (not user-facing)
SKIP_WORDS = {'className', 'onClick', 'onChange', 'useState', 'useEffect', 'import', 'export', 'const', 'function'}


def slugify(text):
    """Convert text to translation key."""
    key = text.lower().strip()
    key = re.sub(r'[^a-z0-9\s]', '', key)
    key = re.sub(r'\s+', '_', key)
    return key[:50]  # Limit key length


def scan_file(filepath):
    """Extract hardcoded strings from a file."""
    suffix = filepath.suffix.lower()
    if suffix not in EXTRACTION_PATTERNS:
        return []

    found = []
    try:
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()

        for pattern in EXTRACTION_PATTERNS[suffix]:
            for match in pattern.finditer(content):
                text = match.group(1).strip()

                # Filter out non-user-facing strings
                if len(text) < 3 or len(text) > 200:
                    continue
                if any(skip in text for skip in SKIP_WORDS):
                    continue
                if text.startswith(('http', '//', '/*', '#', 'import')):
                    continue

                line_num = content[:match.start()].count('\n') + 1
                found.append({
                    'text': text,
                    'line': line_num,
                    'key': slugify(text),
                })
    except Exception:
        pass

    return found


def scan_project(path):
    """Scan project for hardcoded strings."""
    results = defaultdict(list)  # filepath -> list of strings
    root = Path(path)

    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]

        for filename in filenames:
            filepath = Path(dirpath) / filename
            if filepath.suffix.lower() in EXTRACTION_PATTERNS:
                strings = scan_file(filepath)
                if strings:
                    rel_path = str(filepath.relative_to(root))
                    results[rel_path] = strings

    return results


def generate_translation_file(results, output_dir):
    """Generate en.json translation file."""
    output = Path(output_dir)
    output.mkdir(parents=True, exist_ok=True)

    translations = {}
    report = []

    for filepath, strings in sorted(results.items()):
        report.append(f'\n📄 {filepath}:')
        for s in strings:
            key = s['key']
            # Handle duplicate keys
            if key in translations and translations[key] != s['text']:
                key = f"{key}_{s['line']}"
            translations[key] = s['text']
            report.append(f"  L{s['line']}: \"{s['text']}\" → {key}")

    # Write en.json
    en_file = output / 'en.json'
    with open(en_file, 'w', encoding='utf-8') as f:
        json.dump(translations, f, indent=2, ensure_ascii=False)

    return en_file, translations, report


def main():
    parser = argparse.ArgumentParser(description='Extract hardcoded strings for i18n')
    parser.add_argument('--path', default='src/', help='Source path to scan')
    parser.add_argument('--output', default='locales/', help='Output directory for translation files')
    args = parser.parse_args()

    print(f'🔍 Scanning {args.path} for hardcoded strings...')
    results = scan_project(args.path)

    if not results:
        print('No hardcoded strings found.')
        return

    total = sum(len(v) for v in results.values())
    print(f'📦 Found {total} strings in {len(results)} files.')

    en_file, translations, report = generate_translation_file(results, args.output)

    for line in report:
        print(line)

    print(f'\n✅ Generated {en_file} with {len(translations)} translation keys.')
    print(f'💡 Copy {en_file} to create other language files (e.g., vi.json, ja.json)')


if __name__ == '__main__':
    main()
