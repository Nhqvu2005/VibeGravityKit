#!/usr/bin/env python3
"""
Deployment Wizard — Cloudflare Tunnel (cloudflared)
Expose any local website/server to the internet instantly.
Zero hosting, zero domain, zero config needed.

Usage (Human):
    python tunnel.py --port 3000
    python tunnel.py --port 8080 --install
    python tunnel.py --check

Usage (AI Agent - quiet mode):
    python tunnel.py --port 3000 --quiet
    → outputs ONLY: TUNNEL_URL=https://xxx.trycloudflare.com
"""

import argparse
import json
import os
import platform
import re
import shutil
import subprocess
import sys
import time
import urllib.request
import tempfile
from pathlib import Path


# ─── Platform Detection ────────────────────────────────────────

def get_platform_info():
    """Detect OS and architecture."""
    system = platform.system().lower()
    machine = platform.machine().lower()

    arch_map = {
        "x86_64": "amd64", "amd64": "amd64",
        "arm64": "arm64", "aarch64": "arm64",
        "armv7l": "arm", "x86": "386", "i686": "386"
    }
    arch = arch_map.get(machine, "amd64")

    return system, arch


def get_download_url():
    """Get the correct cloudflared download URL for current platform."""
    system, arch = get_platform_info()

    base = "https://github.com/cloudflare/cloudflared/releases/latest/download"

    urls = {
        ("windows", "amd64"): f"{base}/cloudflared-windows-amd64.exe",
        ("windows", "386"):   f"{base}/cloudflared-windows-386.exe",
        ("linux", "amd64"):   f"{base}/cloudflared-linux-amd64",
        ("linux", "arm64"):   f"{base}/cloudflared-linux-arm64",
        ("linux", "arm"):     f"{base}/cloudflared-linux-arm",
        ("darwin", "amd64"):  f"{base}/cloudflared-darwin-amd64.tgz",
        ("darwin", "arm64"):  f"{base}/cloudflared-darwin-amd64.tgz",
    }

    return urls.get((system, arch))


# ─── Installation ──────────────────────────────────────────────

def find_cloudflared():
    """Check if cloudflared is installed and return its path."""
    path = shutil.which("cloudflared")
    if path:
        return path

    system = platform.system().lower()
    common_paths = []

    if system == "windows":
        common_paths = [
            Path(os.environ.get("LOCALAPPDATA", "")) / "cloudflared" / "cloudflared.exe",
            Path(os.environ.get("PROGRAMFILES", "")) / "cloudflared" / "cloudflared.exe",
            Path.home() / ".cloudflared" / "cloudflared.exe",
        ]
    elif system == "linux":
        common_paths = [
            Path("/usr/local/bin/cloudflared"),
            Path("/usr/bin/cloudflared"),
            Path.home() / ".local" / "bin" / "cloudflared",
        ]
    elif system == "darwin":
        common_paths = [
            Path("/usr/local/bin/cloudflared"),
            Path("/opt/homebrew/bin/cloudflared"),
        ]

    for p in common_paths:
        if p.exists():
            return str(p)

    return None


def install_cloudflared(quiet=False):
    """Download and install cloudflared."""
    system, arch = get_platform_info()
    url = get_download_url()

    if not url:
        if quiet:
            print(f"ERROR=unsupported_platform ({system}/{arch})")
        else:
            print(f"❌ Unsupported platform: {system}/{arch}")
            print("   Install manually: https://developers.cloudflare.com/cloudflare-one/connections/connect-networks/downloads/")
        return None

    if not quiet:
        print(f"📥 Downloading cloudflared for {system}/{arch}...")
        print(f"   URL: {url}")

    # Determine install location
    if system == "windows":
        install_dir = Path(os.environ.get("LOCALAPPDATA", Path.home())) / "cloudflared"
        install_dir.mkdir(parents=True, exist_ok=True)
        binary_path = install_dir / "cloudflared.exe"
    else:
        install_dir = Path.home() / ".local" / "bin"
        install_dir.mkdir(parents=True, exist_ok=True)
        binary_path = install_dir / "cloudflared"

    try:
        if url.endswith(".tgz"):
            with tempfile.NamedTemporaryFile(suffix=".tgz", delete=False) as tmp:
                urllib.request.urlretrieve(url, tmp.name)
                import tarfile
                with tarfile.open(tmp.name, "r:gz") as tar:
                    tar.extractall(str(install_dir))
                os.unlink(tmp.name)
        else:
            urllib.request.urlretrieve(url, str(binary_path))

        if system != "windows":
            os.chmod(str(binary_path), 0o755)

        if quiet:
            print(f"INSTALLED={binary_path}")
        else:
            print(f"✅ Installed: {binary_path}")
            if system == "windows":
                print(f"\n💡 To add to PATH: setx PATH \"%PATH%;{install_dir}\"")

        return str(binary_path)

    except Exception as e:
        if quiet:
            print(f"ERROR=download_failed ({e})")
        else:
            print(f"❌ Download failed: {e}")
            print("\n📋 Manual install:")
            if system == "windows":
                print("   winget install --id Cloudflare.cloudflared")
            elif system == "darwin":
                print("   brew install cloudflared")
            else:
                print(f"   curl -L {url} -o /usr/local/bin/cloudflared && chmod +x /usr/local/bin/cloudflared")
        return None


def get_version(binary_path):
    """Get cloudflared version."""
    try:
        result = subprocess.run(
            [binary_path, "version"],
            capture_output=True, text=True, timeout=10
        )
        return result.stdout.strip().split("\n")[0]
    except Exception:
        return "unknown"


# ─── Tunnel Management ─────────────────────────────────────────

def start_tunnel(binary_path, port, protocol="http", metrics_port=None, quiet=False):
    """
    Start a Cloudflare Quick Tunnel.
    In quiet mode: outputs ONLY the URL line, then keeps tunnel alive.
    In normal mode: shows full UI with instructions.
    """
    url = f"{protocol}://localhost:{port}"
    cmd = [binary_path, "tunnel", "--url", url]

    if metrics_port:
        cmd.extend(["--metrics", f"localhost:{metrics_port}"])

    if not quiet:
        print("\n" + "=" * 60)
        print("🚀 CLOUDFLARE TUNNEL")
        print("=" * 60)
        print(f"   Local:    {url}")
        print(f"   Binary:   {binary_path}")
        print(f"   Version:  {get_version(binary_path)}")
        print("=" * 60)
        print()
        print("⏳ Starting tunnel... (waiting for public URL)")
        print("   Press Ctrl+C to stop.\n")

    try:
        process = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1
        )

        tunnel_url = None
        url_found = False

        for line in iter(process.stdout.readline, ""):
            line = line.strip()

            # Detect the tunnel URL
            if ".trycloudflare.com" in line and not url_found:
                urls = re.findall(r'https://[a-zA-Z0-9-]+\.trycloudflare\.com', line)
                if urls:
                    tunnel_url = urls[0]
                    url_found = True

                    if quiet:
                        # Agent mode: output ONLY the parseable line
                        print(f"TUNNEL_URL={tunnel_url}")
                        sys.stdout.flush()
                    else:
                        print("\n" + "=" * 60)
                        print("✅ TUNNEL ACTIVE!")
                        print("=" * 60)
                        print(f"\n   🌐 Public URL:  {tunnel_url}")
                        print(f"   🏠 Local:       {url}")
                        print(f"\n   📋 Share this URL with anyone!")
                        print(f"   ⚠️  URL changes each time you restart.")
                        print(f"   Press Ctrl+C to stop.\n")
                        print("=" * 60)

            # Show errors (even in quiet mode, they matter)
            if not url_found and any(kw in line.lower() for kw in ["err", "fail", "refused"]):
                if quiet:
                    print(f"ERROR={line}")
                else:
                    print(f"   ⚠️  {line}")

        process.wait()

    except KeyboardInterrupt:
        if not quiet:
            print("\n\n🛑 Tunnel stopped.")
            if tunnel_url:
                print(f"   URL {tunnel_url} is no longer active.")
        process.terminate()
        try:
            process.wait(timeout=5)
        except Exception:
            process.kill()

    except Exception as e:
        if quiet:
            print(f"ERROR={e}")
        else:
            print(f"\n❌ Error: {e}")
            if "refused" in str(e).lower():
                print(f"   Make sure your local server is running on port {port}!")


# ─── Status Check ──────────────────────────────────────────────

def check_status(quiet=False):
    """Check cloudflared installation status."""
    system, arch = get_platform_info()
    binary = find_cloudflared()

    if quiet:
        if binary:
            version = get_version(binary)
            print(f"STATUS=installed")
            print(f"BINARY={binary}")
            print(f"VERSION={version}")
        else:
            print(f"STATUS=not_installed")
        return binary is not None

    print("\n" + "=" * 60)
    print("🔍 CLOUDFLARED STATUS CHECK")
    print("=" * 60)
    print(f"   Platform: {system}/{arch}")

    if binary:
        print(f"   ✅ Installed: {binary}")
        print(f"   📦 Version: {get_version(binary)}")
    else:
        print(f"   ❌ Not installed")
        print(f"   Run: python tunnel.py --install")

    print("=" * 60 + "\n")
    return binary is not None


# ─── Main ──────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="Deployment Wizard — Expose local websites via Cloudflare Tunnel",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python tunnel.py --port 3000              # Expose localhost:3000
  python tunnel.py --port 8080 --install    # Install cloudflared + start tunnel
  python tunnel.py --check                  # Check installation
  python tunnel.py --port 3000 --quiet      # Agent mode: output only TUNNEL_URL=...

How it works:
  1. Downloads cloudflared (if needed)
  2. Creates a temporary Cloudflare Tunnel
  3. Gives you a public *.trycloudflare.com URL
  4. No account, no domain, no hosting needed!

Agent (--quiet) mode output format:
  INSTALLED=/path/to/cloudflared       (if installed)
  TUNNEL_URL=https://xxx.trycloudflare.com  (when tunnel is ready)
  ERROR=message                        (if something fails)
        """
    )
    parser.add_argument(
        "--port", "-p", type=int,
        help="Local port to expose (e.g., 3000, 8080, 5173)"
    )
    parser.add_argument(
        "--protocol", type=str, default="http",
        choices=["http", "https"],
        help="Protocol for local server (default: http)"
    )
    parser.add_argument(
        "--install", "-i", action="store_true",
        help="Install cloudflared if not found"
    )
    parser.add_argument(
        "--check", action="store_true",
        help="Check cloudflared installation status"
    )
    parser.add_argument(
        "--quiet", "-q", action="store_true",
        help="Agent mode: output only machine-parseable lines (TUNNEL_URL=, ERROR=, STATUS=)"
    )
    parser.add_argument(
        "--metrics-port", type=int, default=None,
        help="Port for cloudflared metrics server"
    )

    args = parser.parse_args()

    # Status check
    if args.check:
        check_status(quiet=args.quiet)
        return

    # Find or install cloudflared
    binary = find_cloudflared()

    if not binary:
        if args.install or args.port:
            if not args.quiet:
                print("⚠️  cloudflared not found. Installing...")
            binary = install_cloudflared(quiet=args.quiet)
            if not binary:
                sys.exit(1)
        else:
            if args.quiet:
                print("ERROR=not_installed")
            else:
                print("❌ cloudflared not found.")
                print("   Run: python tunnel.py --install")
            sys.exit(1)

    # Start tunnel
    if args.port:
        start_tunnel(binary, args.port, args.protocol, args.metrics_port, quiet=args.quiet)
    elif args.install:
        if args.quiet:
            print(f"INSTALLED={binary}")
        else:
            print(f"✅ cloudflared ready: {binary}")
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
