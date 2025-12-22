<h2 align="center">
	osu!droid Server
</h2>

<h>VERY OUTDATED README, NEEDS TO BE REWRITTEN</h>

<h4 align="center">
        meme server <br/>
        <a href="https://www.codefactor.io/repository/github/fireredz/yuzumi"><img src="https://www.codefactor.io/repository/github/fireredz/yuzumi/badge" alt="CodeFactor" /></a>
</h4>

<p align="center">
	<img height=300 src="https://cdn.discordapp.com/attachments/716590826729504788/818733799256621056/yuzumi_yuzuhara.jpg" alt="lole">
</p>



## Features
* ✅ **Fully-working** osu!droid server with relax mod support
* 🏆 **PP System** with performance points calculation
* 🌍 **Automatic Country Detection** via IP geolocation
* 🏴 **National Flags** displayed on user profiles
* 🎮 **Multiplayer Support** with real-time rooms and spectating
* 🔐 **Secure Authentication** with Argon2 password hashing
* 🌐 **Web Interface** for user registration, login, and profile management
* 📊 **Leaderboards** with global and country rankings
* 🎵 **Beatmap Management** with automatic status updates
* 🤖 **Discord Integration** for webhook notifications
* 📱 **Mobile Optimized** web interface

## Todo
* MySQL Support

## Preview (with PP system)
[Video Gameplay](https://youtu.be/NF9VeNyj_gA)
![Main Menu](https://cdn.discordapp.com/attachments/703552229680087042/818712990916411432/Screenshot_2021-03-09-13-09-54-85.jpg)
![Leaderboard(pp)](https://cdn.discordapp.com/attachments/703552229680087042/818712991201361950/Screenshot_2021-03-09-13-11-09-33.jpg)
![Play Submit](https://cdn.discordapp.com/attachments/703552229680087042/818712991435456522/Screenshot_2021-03-09-13-12-30-75.jpg)

## Requirements

### System Requirements
* **Python 3.8+** (Recommended: Python 3.11+)
* **PostgreSQL** database server
* **Rust** compiler (automatically installed by setup script)
* **Linux/macOS** (primary support) or Windows with WSL

### Automatic Setup
The `start.sh` script handles all dependencies automatically:
- ✅ Rust installation and setup
- ✅ Python dependencies installation
- ✅ GeoLite2 database download
- ✅ Database initialization
- ✅ Directory structure creation
- ✅ Server startup

### Manual Installation
If you prefer manual setup:
```bash
# Install Python dependencies
pip install -r requirements.txt

# Install Rust (if needed)
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh

# Install PostgreSQL
# Ubuntu/Debian: sudo apt install postgresql
# macOS: brew install postgresql
# Windows: Download from postgresql.org
```

## Setting up (server)

### Quick Start (Recommended)
Run the automated setup script:
```bash
./start.sh
```
This script will:
- Install Rust (if needed)
- Install all Python dependencies
- Download GeoLite2 database for country detection
- Setup database and create .env file
- Create necessary directories
- Start the server automatically

### Manual Setup
If you prefer manual installation:

1. **Install Dependencies:**
```bash
pip install -r requirements.txt
# Or use the Python installer
python install_deps.py
```

2. **Setup Environment:**
Create a `.env` file with your configuration:
```env
SERVER_PORT=8080
SERVER_IP=127.0.0.1
DATABASE_URL=postgresql://postgres:password@localhost:5432/osudroid
```

3. **Setup Database:**
```bash
# Create database
createdb -U postgres osudroid

# Setup database user and permissions
psql -U postgres -c "ALTER USER postgres PASSWORD 'your_password';"
```

4. **Run the Server:**
```bash
python main.py
```

### Features
- 🌍 **Automatic Country Detection** via IP geolocation
- 🏴 **National Flags** displayed on user profiles
- 📊 **PP System** with performance points calculation
- 🎮 **Multiplayer Support** with real-time rooms
- 🔐 **Secure Authentication** with password hashing
- 🌐 **Web Interface** for user management

## Setting up (client)
There's two way of doing this, hosts and modified .apk. <br/>
Hosts method is better since you can change between servers without downloading apks.

### Hosts
* Install [Hosts Go](https://play.google.com/store/apps/details?id=dns.hosts.server.change&hl=en&gl=US) from Google Play or other site
* Add `ops.dgsrz.com` with your server ip address.
* That's it

### Apk
There's also two way of doing this, build from sources and modified .apk.<br/>
Since I don't commit java, we're going with the latter.

You need java installed for this (the same one that you need for Minecraft :>)

Update: There's a script for this now, you can use that if you're retarded or lazy like me <br/>
[[Script]](https://github.com/FireRedz/osudroid-patch) <br/>
[[Manual]](https://github.com/FireRedz/osudroid-patch/blob/master/old.md)



## Disclaimer
im retarded
