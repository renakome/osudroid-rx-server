#!/usr/bin/env python3
"""
Script to install dependencies in correct order
Use this script instead of pip install -r requirements.txt
"""
import subprocess
import sys
import os

def run_command(cmd, description):
    """Execute command and show result"""
    print(f"🔧 {description}: {' '.join(cmd)}")
    try:
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        print(f"✅ {description}: OK")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description}: FAILED")
        print(f"Error: {e.stderr}")
        return False

def main():
    print("📦 Installing osu!droid RX Server dependencies")
    print("=" * 55)

    # Step 1: Install maturin first
    if not run_command([sys.executable, "-m", "pip", "install", "maturin>=1.0.0"],
                      "Installing maturin (build tool)"):
        return False

    # Step 2: Install rosu-pp-py separately
    if not run_command([sys.executable, "-m", "pip", "install", "git+https://github.com/unclem2/rosu-pp-py"],
                      "Installing rosu-pp-py (PP calculator)"):
        return False

    # Step 3: Install rest of dependencies (except rosu-pp-py)
    deps_to_install = [
        "aiohttp~=3.10.5",
        "asyncpg",
        "coloredlogs==15.0.1",
        "Hypercorn==0.17.3",
        "python-dotenv==1.0.1",
        "python-socketio~=5.11.4",
        "Quart~=0.19.6",
        "Werkzeug~=3.0.4",
        "discord-webhook[async]==1.3.1",
        "geoip2==4.8.1",
        "pytest~=8.3.4",
        "requests~=2.32.3",
        "javaobj-py3~=0.4.4",
        # "Mailgun==0.1.0",  # Removed for now
    ]

    # Install in smaller batches to avoid issues
    batch_size = 5
    for i in range(0, len(deps_to_install), batch_size):
        batch = deps_to_install[i:i+batch_size]
        if not run_command([sys.executable, "-m", "pip", "install"] + batch,
                          f"Installing batch {i//batch_size + 1} of dependencies"):
            return False

    print("\n🎉 All dependencies installed successfully!")
    print("🚀 You can now run: python main.py")

    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
