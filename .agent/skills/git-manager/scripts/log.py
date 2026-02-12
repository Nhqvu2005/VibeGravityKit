#!/usr/bin/env python3
"""
Git Manager — Leader Log Report.

Usage:
    python log.py [--limit 10]
"""

import argparse
import subprocess

def get_log(limit):
    # Format: Hash - Author, Time : Subject
    fmt = "%h - %an, %ar : %s"
    cmd = ["git", "log", f"-n {limit}", f"--pretty=format:{fmt}"]
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    print("\n📜 Project History (Recent):\n")
    print(result.stdout)
    print("\n")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--limit", type=int, default=10)
    args = parser.parse_args()
    get_log(args.limit)

if __name__ == "__main__":
    main()
