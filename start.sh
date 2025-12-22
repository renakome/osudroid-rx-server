#!/bin/bash
# Complete setup and startup script for osu!droid RX Server
# This script installs all dependencies and starts the server

echo "🚀 Starting osu!droid RX Server Setup"
echo "====================================="

# Check if running on supported OS
if [[ "$OSTYPE" != "linux-gnu"* ]] && [[ "$OSTYPE" != "darwin"* ]]; then
    echo "⚠️  Warning: This script is optimized for Linux/macOS"
    echo "   On Windows, consider using install_deps.py instead"
fi

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Function to install Rust
install_rust() {
    echo "🦀 Installing Rust..."
    if command_exists curl; then
        curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y --default-toolchain stable --profile minimal
        export PATH="$HOME/.cargo/bin:$PATH"
        echo "✅ Rust installed successfully"
    else
        echo "❌ curl not found. Please install curl or Rust manually"
        exit 1
    fi
}

# Function to install Python dependencies
install_python_deps() {
    echo "📦 Installing Python dependencies..."

    # Check if pip is available
    if ! command_exists pip; then
        echo "❌ pip not found. Please install Python and pip first"
        exit 1
    fi

    # Install maturin first
    echo "🔧 Installing maturin..."
    pip install maturin>=1.0.0 || {
        echo "❌ Failed to install maturin"
        exit 1
    }

    # Install rosu-pp-py
    echo "🎯 Installing rosu-pp-py..."
    pip install git+https://github.com/unclem2/rosu-pp-py || {
        echo "❌ Failed to install rosu-pp-py"
        exit 1
    }

    # Install remaining dependencies in batches to avoid issues
    echo "📚 Installing remaining dependencies..."

    # Batch 1
    pip install aiohttp~=3.10.5 asyncpg coloredlogs==15.0.1 Hypercorn==0.17.3 python-dotenv==1.0.1 || {
        echo "❌ Failed to install batch 1 dependencies"
        exit 1
    }

    # Batch 2
    pip install python-socketio~=5.11.4 Quart~=0.19.6 quart-schema~=0.18.0 argon2-cffi~=23.1.0 || {
        echo "❌ Failed to install batch 2 dependencies"
        exit 1
    }

    # Batch 3
    pip install Werkzeug~=3.0.4 discord-webhook[async]==1.3.1 geoip2==4.8.1 || {
        echo "❌ Failed to install batch 3 dependencies"
        exit 1
    }

    # Batch 4
    pip install pytest~=8.3.4 requests~=2.32.3 javaobj-py3~=0.4.4 || {
        echo "❌ Failed to install batch 4 dependencies"
        exit 1
    }

    echo "✅ All Python dependencies installed successfully"
}

# Function to download GeoLite2 database
download_geolite() {
    echo "🌍 Downloading GeoLite2 Country database..."

    # Try multiple sources for GeoLite2
    if command_exists curl; then
        # Try primary source
        if curl -L -o GeoLite2-Country.mmdb "https://cdn.jsdelivr.net/gh/Hackl0us/GeoIP2-CN@release/Country.mmdb" 2>/dev/null; then
            echo "✅ GeoLite2 database downloaded successfully"
            return 0
        fi

        # Try alternative source
        if curl -L -o GeoLite2-Country.mmdb "https://github.com/P3TERX/GeoLite.mmdb/raw/download/GeoLite2-Country.mmdb" 2>/dev/null; then
            echo "✅ GeoLite2 database downloaded successfully (alternative source)"
            return 0
        fi
    fi

    echo "⚠️  Warning: Could not download GeoLite2 database"
    echo "   Country detection will use online API fallback only"
    return 1
}

# Function to check if PostgreSQL is running
check_postgres() {
    echo "🐘 Checking PostgreSQL..."

    if command_exists psql; then
        if psql -U postgres -c "SELECT version();" >/dev/null 2>&1; then
            echo "✅ PostgreSQL is running"
            return 0
        else
            echo "⚠️  PostgreSQL is installed but not running"
            echo "   Please start PostgreSQL service:"
            echo "   - Linux: sudo systemctl start postgresql"
            echo "   - macOS: brew services start postgresql"
            return 1
        fi
    else
        echo "⚠️  PostgreSQL not found"
        echo "   Please install PostgreSQL:"
        echo "   - Ubuntu/Debian: sudo apt install postgresql postgresql-contrib"
        echo "   - CentOS/RHEL: sudo yum install postgresql-server postgresql-contrib"
        echo "   - macOS: brew install postgresql"
        return 1
    fi
}

# Function to setup database
setup_database() {
    echo "🗄️  Setting up database..."

    # Check if .env exists
    if [ ! -f ".env" ]; then
        echo "📝 Creating .env file..."
        cat > .env << EOF
# Server Configuration
SERVER_PORT=8080
SERVER_IP=127.0.0.1
SERVER_DOMAIN=

# Database Configuration
DATABASE_URL=postgresql://postgres:password@localhost:5432/osudroid

# External API Keys (optional for basic functionality)
OSU_KEY=
SUBMIT_DISCORD=
WL_DISCORD=
WL_KEY=
LOGIN_KEY=
EOF
        echo "✅ .env file created"
    else
        echo "✅ .env file already exists"
    fi

    # Try to create database if PostgreSQL is available
    if command_exists psql; then
        echo "📦 Setting up database schema..."
        if psql -U postgres -c "CREATE DATABASE osudroid;" 2>/dev/null; then
            echo "✅ Database 'osudroid' created"
        else
            echo "ℹ️  Database 'osudroid' may already exist"
        fi
    fi
}

# Function to start the server
start_server() {
    echo ""
    echo "🚀 Starting osu!droid RX Server..."
    echo "=================================="

    # Check if main.py exists
    if [ ! -f "main.py" ]; then
        echo "❌ main.py not found in current directory"
        exit 1
    fi

    # Check if Python is available
    if ! command_exists python3 && ! command_exists python; then
        echo "❌ Python not found"
        exit 1
    fi

    # Try to run the server
    if command_exists python3; then
        echo "🐍 Starting server with python3..."
        python3 main.py
    else
        echo "🐍 Starting server with python..."
        python main.py
    fi
}

# Main execution
main() {
    echo "🔍 Checking system requirements..."

    # Check Python
    if ! command_exists python3 && ! command_exists python; then
        echo "❌ Python not found. Please install Python 3.8+ first"
        exit 1
    fi

    # Install Rust if needed
    if ! command_exists rustc; then
        install_rust
    else
        echo "✅ Rust already installed"
    fi

    # Install Python dependencies
    install_python_deps

    # Try to download GeoLite2 database
    download_geolite

    # Setup database
    setup_database

    # Check PostgreSQL
    check_postgres

    # Create necessary directories
    echo "📁 Creating necessary directories..."
    mkdir -p data/avatar data/beatmaps data/replays
    echo "✅ Directories created"

    echo ""
    echo "🎉 Setup completed successfully!"
    echo "================================"

    # Start the server
    start_server
}

# Run main function
main "$@"
