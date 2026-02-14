#!/usr/bin/env python3
"""
Deployment Wizard — Cloudflare Tunnel (cloudflared)
Expose any local website/server to the internet instantly.
Zero hosting, zero domain, zero config needed.

Usage:
    python tunnel.py --port 3000
    python tunnel.py --port 8080 --install
    python tunnel.py --check
    python tunnel.py --port 5173 --protocol http
"""

import argparse
import json
import os
import platform
import shutil
import subprocess
import sys
import time
import urllib.request
import zipfile
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
    # Check PATH
    path = shutil.which("cloudflared")
    if path:
        return path

    # Check common locations
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


def install_cloudflared():
    """Download and install cloudflared."""
    system, arch = get_platform_info()
    url = get_download_url()

    if not url:
        print(f"❌ Unsupported platform: {system}/{arch}")
        print("   Please install cloudflared manually:")
        print("   https://developers.cloudflare.com/cloudflare-one/connections/connect-networks/downloads/")
        return None

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
            # macOS: download and extract tarball
            with tempfile.NamedTemporaryFile(suffix=".tgz", delete=False) as tmp:
                urllib.request.urlretrieve(url, tmp.name)
                import tarfile
                with tarfile.open(tmp.name, "r:gz") as tar:
                    tar.extractall(str(install_dir))
                os.unlink(tmp.name)
        else:
            # Windows/Linux: direct binary download
            urllib.request.urlretrieve(url, str(binary_path))

        # Make executable on Unix
        if system != "windows":
            os.chmod(str(binary_path), 0o755)

        print(f"✅ Installed: {binary_path}")

        # Add to PATH hint
        if system == "windows":
            print(f"\n💡 To add to PATH permanently, run:")
            print(f'   setx PATH "%PATH%;{install_dir}"')
        else:
            path_dirs = os.environ.get("PATH", "").split(":")
            if str(install_dir) not in path_dirs:
                print(f"\n💡 Add to PATH: export PATH=\"{install_dir}:$PATH\"")

        return str(binary_path)

    except Exception as e:
        print(f"❌ Download failed: {e}")
        print("\n📋 Manual install options:")
        if system == "windows":
            print("   winget install --id Cloudflare.cloudflared")
            print("   choco install cloudflared")
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

def start_tunnel(binary_path, port, protocol="http", metrics_port=None):
    """
    Start a Cloudflare Quick Tunnel.
    This creates a temporary public URL that routes to localhost:port.
    No Cloudflare account needed!
    """
    url = f"{protocol}://localhost:{port}"

    print("\n" + "=" * 60)
    print("🚀 CLOUDFLARE TUNNEL")
    print("=" * 60)
    print(f"   Local:    {url}")
    print(f"   Binary:   {binary_path}")
    print(f"   Version:  {get_version(binary_path)}")
    print("=" * 60)
    print()
    print("⏳ Starting tunnel... (waiting for public URL)")
    print("   Press Ctrl+C to stop the tunnel.\n")

    cmd = [binary_path, "tunnel", "--url", url]

    if metrics_port:
        cmd.extend(["--metrics", f"localhost:{metrics_port}"])

    try:
        process = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1
        )

        tunnel_url = None

        for line in iter(process.stdout.readline, ""):
            line = line.strip()

            # Detect the tunnel URL from cloudflared output
            if ".trycloudflare.com" in line:
                # Extract URL
                import re
                urls = re.findall(r'https://[a-zA-Z0-9-]+\.trycloudflare\.com', line)
                if urls:
                    tunnel_url = urls[0]
                    print("\n" + "=" * 60)
                    print("✅ TUNNEL ACTIVE!")
                    print("=" * 60)
                    print(f"\n   🌐 Public URL:  {tunnel_url}")
                    print(f"   🏠 Local:       {url}")
                    print(f"\n   📋 Share this URL with anyone to access your local site!")
                    print(f"   ⚠️  URL changes each time you restart the tunnel.")
                    print(f"   Press Ctrl+C to stop.\n")
                    print("=" * 60)

            # Show important logs (errors, warnings)
            if any(kw in line.lower() for kw in ["err", "warn", "fail", "refused"]):
                print(f"   ⚠️  {line}")

        process.wait()

    except KeyboardInterrupt:
        print("\n\n🛑 Tunnel stopped.")
        if tunnel_url:
            print(f"   URL {tunnel_url} is no longer active.")
        process.terminate()
        process.wait(timeout=5)

    except Exception as e:
        print(f"\n❌ Error: {e}")
        if "refused" in str(e).lower():
            print(f"   Make sure your local server is running on port {port}!")


# ─── Status Check ──────────────────────────────────────────────

def check_status():
    """Check cloudflared installation status."""
    print("\n" + "=" * 60)
    print("🔍 CLOUDFLARED STATUS CHECK")
    print("=" * 60)

    system, arch = get_platform_info()
    print(f"   Platform: {system}/{arch}")

    binary = find_cloudflared()
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
  python tunnel.py --check                  # Check if cloudflared is installed
  python tunnel.py --port 5173 --protocol http

How it works:
  1. Downloads cloudflared (if needed)
  2. Creates a temporary Cloudflare Tunnel
  3. Gives you a public *.trycloudflare.com URL
  4. Anyone can access your local site via that URL
  5. No account, no domain, no hosting needed!
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
        "--metrics-port", type=int, default=None,
        help="Port for cloudflared metrics server"
    )

    args = parser.parse_args()

    # Status check
    if args.check:
        check_status()
        return

    # Find or install cloudflared
    binary = find_cloudflared()

    if not binary:
        if args.install or args.port:
            print("⚠️  cloudflared not found. Installing...")
            binary = install_cloudflared()
            if not binary:
                sys.exit(1)
        else:
            print("❌ cloudflared not found.")
            print("   Run: python tunnel.py --install")
            print("   Or:  python tunnel.py --port 3000 --install")
            sys.exit(1)

    # Start tunnel
    if args.port:
        start_tunnel(binary, args.port, args.protocol, args.metrics_port)
    elif not args.install and not args.check:
        parser.print_help()


if __name__ == "__main__":
    main()
