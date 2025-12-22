#!/bin/bash
# Simple installation script for ShardCloud
# This avoids shebang issues with Python scripts

echo "📦 Installing osu!droid RX Server dependencies"
echo "==============================================="

# Install Rust if not present
echo "🦀 Checking Rust..."
if ! command -v rustc &> /dev/null; then
    echo "📥 Installing Rust..."
    curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y --default-toolchain stable --profile minimal
    export PATH="$HOME/.cargo/bin:$PATH"
    echo "✅ Rust installed"
else
    echo "✅ Rust already installed"
fi

# Install Python dependencies
echo "📦 Installing Python dependencies..."

# Install maturin
pip install maturin>=1.0.0

# Install rosu-pp-py
pip install git+https://github.com/unclem2/rosu-pp-py

# Install remaining dependencies
pip install aiohttp~=3.10.5 asyncpg coloredlogs==15.0.1 Hypercorn==0.17.3
pip install python-dotenv==1.0.1 python-socketio~=5.11.4 Quart~=0.19.6
pip install Werkzeug~=3.0.4 discord-webhook[async]==1.3.1 geoip2==4.8.1
pip install pytest~=8.3.4 requests~=2.32.3 javaobj-py3~=0.4.4

echo ""
echo "🎉 All dependencies installed successfully!"
echo "🚀 You can now run: python main.py"
