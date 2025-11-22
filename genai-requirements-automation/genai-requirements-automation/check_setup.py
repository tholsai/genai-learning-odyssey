"""Diagnostic script to check setup issues."""
import sys
import subprocess
import os
from pathlib import Path

def check_python_version():
    """Check Python version."""
    print("=" * 60)
    print("1. Checking Python Version")
    print("=" * 60)
    version = sys.version_info
    print(f"Python version: {version.major}.{version.minor}.{version.micro}")
    if version.major < 3 or (version.major == 3 and version.minor < 10):
        print("[ERROR] Python 3.10+ is required!")
        return False
    print("[OK] Python version is compatible")
    return True

def check_uv_installed():
    """Check if uv is installed."""
    print("\n" + "=" * 60)
    print("2. Checking UV Installation")
    print("=" * 60)
    try:
        result = subprocess.run(
            ["uv", "--version"],
            capture_output=True,
            text=True,
            timeout=5
        )
        if result.returncode == 0:
            print(f"[OK] UV is installed: {result.stdout.strip()}")
            return True
        else:
            print("[ERROR] UV is not working properly")
            return False
    except FileNotFoundError:
        print("[ERROR] UV is not installed!")
        print("   Install from: https://github.com/astral-sh/uv")
        return False
    except Exception as e:
        print(f"[ERROR] Error checking UV: {e}")
        return False

def check_pyproject_toml():
    """Check if pyproject.toml exists and is valid."""
    print("\n" + "=" * 60)
    print("3. Checking pyproject.toml")
    print("=" * 60)
    if not Path("pyproject.toml").exists():
        print("[ERROR] pyproject.toml not found!")
        return False
    
    print("[OK] pyproject.toml exists")
    
    # Try to parse it
    try:
        import tomli
        with open("pyproject.toml", "rb") as f:
            data = tomli.load(f)
        print("[OK] pyproject.toml is valid TOML")
        
        # Check for common issues
        if "project" not in data:
            print("[ERROR] Missing [project] section")
            return False
        
        if "dependencies" not in data["project"]:
            print("[ERROR] Missing dependencies in [project]")
            return False
        
        print(f"[OK] Found {len(data['project']['dependencies'])} dependencies")
        return True
    except ImportError:
        print("[WARN] Could not validate TOML (tomli not installed)")
        return True
    except Exception as e:
        print(f"[ERROR] Error parsing pyproject.toml: {e}")
        return False

def check_network():
    """Check network connectivity."""
    print("\n" + "=" * 60)
    print("4. Checking Network Connectivity")
    print("=" * 60)
    try:
        import urllib.request
        urllib.request.urlopen("https://pypi.org", timeout=5)
        print("[OK] Network connectivity OK")
        return True
    except Exception as e:
        print(f"[ERROR] Network issue: {e}")
        return False

def try_uv_sync():
    """Try to run uv sync and capture errors."""
    print("\n" + "=" * 60)
    print("5. Attempting uv sync (dry run)")
    print("=" * 60)
    try:
        result = subprocess.run(
            ["uv", "sync", "--dry-run"],
            capture_output=True,
            text=True,
            timeout=30
        )
        if result.returncode == 0:
            print("[OK] uv sync dry-run successful")
            return True, None
        else:
            error = result.stderr or result.stdout
            print(f"[ERROR] uv sync failed:")
            print(error)
            return False, error
    except subprocess.TimeoutExpired:
        print("[ERROR] uv sync timed out")
        return False, "Timeout"
    except Exception as e:
        print(f"[ERROR] Error running uv sync: {e}")
        return False, str(e)

def main():
    """Run all checks."""
    print("\n" + "=" * 60)
    print("GenAI Requirements Automation - Setup Diagnostic")
    print("=" * 60)
    
    checks = [
        check_python_version(),
        check_uv_installed(),
        check_pyproject_toml(),
        check_network(),
    ]
    
    if all(checks):
        success, error = try_uv_sync()
        if not success:
            print("\n" + "=" * 60)
            print("RECOMMENDED FIXES:")
            print("=" * 60)
            if error and "toml" in error.lower():
                print("1. Fix pyproject.toml format")
            elif error and "network" in error.lower():
                print("1. Check your internet connection")
            elif error and "python" in error.lower():
                print("1. Ensure Python 3.10+ is installed")
            else:
                print("1. Try: uv cache clean")
                print("2. Try: uv sync --no-cache")
                print("3. Check the error message above for specific package issues")
    else:
        print("\n" + "=" * 60)
        print("SETUP ISSUES DETECTED")
        print("=" * 60)
        print("Please fix the issues above before running uv sync")

if __name__ == "__main__":
    main()

