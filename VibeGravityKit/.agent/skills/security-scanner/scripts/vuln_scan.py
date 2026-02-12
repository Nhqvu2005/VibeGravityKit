#!/usr/bin/env python3
"""
Security Scanner — Simple Regex SAST (Zero Token).

Usage:
    python vuln_scan.py <dir>
"""

import argparse
import re
import os
from pathlib import Path

PATTERNS = [
    # Secrets
    (r'AWS_SECRET_KEY', 'AWS Key detected (Hardcoded Secret)'),
    (r'BEGIN RSA PRIVATE KEY', 'Private Key detected (Hardcoded Secret)'),
    (r'api_key\s*=\s*[\'"][^\'"]+[\'"]', 'Hardcoded API Key'),
    (r'password\s*=\s*[\'"][^\'"]+[\'"]', 'Hardcoded Password'),
    
    # Injection (SQLi / Command)
    (r'eval\(', 'Code Injection Risk (eval)'),
    (r'exec\(', 'Code Injection Risk (exec)'),
    (r'subprocess\.call\(.*shell=True', 'Command Injection Risk (shell=True)'),
    (r'Expected SQL injection', 'Potential SQL Injection (Raw Query)'), # Placeholder pattern
    
    # XSS (Frontend)
    (r'dangerouslySetInnerHTML', 'XSS Risk (React)'),
    (r'innerHTML\s*=', 'XSS Risk (DOM)'),
    (r'v-html', 'XSS Risk (Vue)'),
    
    # Weak Crypto / Auth
    (r'md5\(', 'Weak Hashing (MD5) - Use bcrypt/argon2'),
    (r'sha1\(', 'Weak Hashing (SHA1)'),
    (r'http://', 'Insecure Protocol (HTTP) - Use HTTPS'),
    (r'Debug\s*=\s*True', 'Debug Mode Enabled in Prod')
]

def scan_file(path):
    issues = []
    try:
        with open(path, 'r', encoding='utf-8') as f:
            for i, line in enumerate(f, 1):
                for pattern, msg in PATTERNS:
                    if re.search(pattern, line):
                        issues.append((i, msg, line.strip()[:100]))
    except:
        pass
    return issues

def scan_dir(root):
    print(f"🛡️  Scanning {root} for vulnerabilities...\n")
    found = False
    for dirpath, _, filenames in os.walk(root):
        if 'node_modules' in dirpath or '.git' in dirpath or '__pycache__' in dirpath:
            continue
            
        for name in filenames:
            path = Path(dirpath) / name
            if path.suffix not in ['.py', '.js', '.ts', '.jsx', '.tsx', '.env', '.json']:
                continue
                
            issues = scan_file(path)
            if issues:
                found = True
                print(f"🚨 {path}:")
                for line, msg, code in issues:
                    print(f"   Line {line}: {msg} -> `{code}`")
                print("")
                
    if not found:
        print("✅ No obvious issues found.")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("dir", default=".")
    args = parser.parse_args()
    scan_dir(args.dir)

if __name__ == "__main__":
    main()
