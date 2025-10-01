# INSTALLATION & SETUP — LINUX

This document combines the comprehensive installation guide and the setup summary for the All-in-One System Tools on Linux systems. It merges the contents of `INSTALL_LINUX.md` and `LINUX_SETUP.md` into a single reference to simplify installation, verification, troubleshooting and development workflows.

## 🚀 Quick Installation

### Automatic Installation (Recommended)

```bash
# Clone the repository
git clone https://github.com/Srijan-XI/AIO-SDMS.git
cd aio-sdms

# Run the setup script
chmod +x setup.sh
./setup.sh
```

### Manual Installation

If you prefer manual install or the automatic script fails, follow these steps:

```bash
# 1. Install system dependencies (Ubuntu/Debian)
sudo apt-get update
sudo apt-get install -y python3-dev python3-venv python3-pip build-essential \
    portaudio19-dev libasound2-dev libsdl2-dev libsdl2-mixer-dev \
    libopencv-dev python3-opencv bluetooth libbluetooth-dev bluez bluez-tools

# 2. Create installation directory
mkdir -p ~/.local/share/allinone-system-tools

# 3. Copy files
cp -r * ~/.local/share/allinone-system-tools/

# 4. Create virtual environment
cd ~/.local/share/allinone-system-tools
python3 -m venv venv

# 5. Install Python dependencies
source venv/bin/activate
pip install -r requirements-linux.txt

# 6. Create launcher script
mkdir -p ~/.local/bin
cat > ~/.local/bin/allinone-tools << 'EOF'
#!/bin/bash
source ~/.local/share/allinone-system-tools/venv/bin/activate
cd ~/.local/share/allinone-system-tools
python main.py "$@"
deactivate
EOF
chmod +x ~/.local/bin/allinone-tools

# 7. Update PATH
echo 'export PATH="$PATH:$HOME/.local/bin"' >> ~/.bashrc
source ~/.bashrc
```

## 📋 System Requirements

### Minimum Requirements
- OS: Linux (any modern distribution)
- Python: 3.7 or higher
- RAM: 512 MB
- Storage: 200 MB free space
- Architecture: x86_64, ARM64

### Recommended Requirements
- OS: Ubuntu 20.04+, Fedora 34+, or equivalent
- Python: 3.9 or higher
- RAM: 1 GB
- Storage: 500 MB free space

## ✅ Supported Distributions (Summary)

Fully tested:
- Ubuntu 20.04, 22.04, 24.04
- Debian 11, 12
- Fedora 36, 37, 38
- CentOS 8, 9
- Arch Linux
- Manjaro

Should work (minor adjustments):
- openSUSE Leap/Tumbleweed
- Linux Mint
- Pop!_OS
- Elementary OS
- Kali Linux

## 🔧 Distribution-Specific Instructions

### Ubuntu/Debian

```bash
sudo apt-get update
sudo apt-get install -y python3-dev python3-venv python3-pip build-essential \
    portaudio19-dev libasound2-dev libsdl2-dev libsdl2-mixer-dev \
    libopencv-dev python3-opencv bluetooth libbluetooth-dev bluez bluez-tools

./setup.sh
```

### Fedora/CentOS/RHEL

```bash
sudo dnf install -y python3-devel gcc gcc-c++ make portaudio-devel \
    alsa-lib-devel SDL2-devel SDL2_mixer-devel opencv-devel \
    python3-opencv bluez bluez-libs-devel

./setup.sh
```

### Arch Linux/Manjaro

```bash
sudo pacman -S python python-pip base-devel portaudio alsa-lib \
    sdl2 sdl2_mixer opencv python-opencv bluez bluez-utils

./setup.sh
```

### openSUSE

```bash
sudo zypper install python3-devel gcc gcc-c++ make portaudio-devel \
    alsa-devel libSDL2-devel libSDL2_mixer-devel opencv-devel \
    python3-opencv bluez bluez-devel

./setup.sh
```

## 🎯 How to Use

### Command Line Interface (CLI)

```bash
allinone-tools                    # Default CLI interface
allinone-tools --cli              # Explicit CLI mode
allinone-tools battery            # Direct battery monitoring
allinone-tools diagnostics        # Hardware diagnostics
allinone-tools monitor            # System monitoring
allinone-tools packages           # Package management
```

### Web Interface

```bash
allinone-tools --web              # Launch web interface
# Access via browser: http://localhost:5000
```

### GUI Interface (Future)

```bash
allinone-tools --gui              # Launch GUI interface
```

## 🔧 Configuration

### Config File Location

```
~/.config/allinone-system-tools/config.json
```

### Default Configuration (example)

```json
{
    "logging": {
        "level": "INFO",
        "file": "~/.local/share/allinone-system-tools/logs/app.log"
    },
    "interfaces": {
        "default": "cli",
        "web": {
            "host": "127.0.0.1",
            "port": 5000,
            "debug": false
        }
    },
    "tools": {
        "battery": {
            "update_interval": 5,
            "enable_notifications": true
        },
        "diagnostics": {
            "auto_detect_hardware": true
        },
        "monitoring": {
            "update_interval": 10,
            "history_length": 100
        }
    }
}
```

## 🔧 Key Features of the Setup Script

- Smart distribution detection (apt/dnf/pacman/zypper)
- Comprehensive dependency management (system libs + Python venv)
- User-friendly install with colored progress and logging
- Desktop integration and launcher creation
- Clean uninstallation support

The `setup.sh` included in the repo performs automatic detection of the distribution and attempts to install the required packages, create a venv, install Python dependencies, create a launcher script and (optionally) desktop integration.

## 🔍 Verification & Testing

After installation, verify the install and test functionality:

```bash
# Test installation
cd ~/.local/share/allinone-system-tools
python3 verify_installation.py

# Run basic checks
allinone-tools --help
allinone-tools battery --test
allinone-tools diagnostics
```

The `verify_installation.py` script checks Python packages, system dependencies, and hardware access.

## 🛠️ Troubleshooting

### Common Issues

#### Permission Errors

```bash
sudo usermod -a -G audio,video,dialout $USER
# Log out and back in for changes to take effect
```

#### Audio/Microphone Issues

```bash
# Check if PulseAudio is running
pulseaudio --check -v

# Restart PulseAudio if needed
pulseaudio -k && pulseaudio --start

# Install additional audio packages if needed (Ubuntu/Debian)
sudo apt-get install pulseaudio pulseaudio-utils
```

#### Camera Issues

```bash
ls -l /dev/video*
sudo usermod -a -G video $USER
sudo apt-get install v4l-utils
v4l2-ctl --list-devices
```

#### Bluetooth Issues

```bash
sudo systemctl status bluetooth
sudo systemctl start bluetooth
sudo systemctl enable bluetooth
sudo systemctl restart bluetooth
```

#### Python Virtual Environment Issues

```bash
rm -rf ~/.local/share/allinone-system-tools/venv
cd ~/.local/share/allinone-system-tools
python3 -m venv venv
source venv/bin/activate
pip install -r requirements-linux.txt
```

### Logs
- Installation Log: `/tmp/allinone-setup.log`
- Application Log: `~/.local/share/allinone-system-tools/logs/app.log`
- Error Log: `~/.local/share/allinone-system-tools/logs/error.log`

## 🗑️ Uninstallation

### Automatic Uninstallation

```bash
~/.local/share/allinone-system-tools/uninstall.sh
```

### Manual Uninstallation

```bash
# Remove installation directory
rm -rf ~/.local/share/allinone-system-tools

# Remove launcher
rm -f ~/.local/bin/allinone-tools

# Remove desktop entry
rm -f ~/.local/share/applications/allinone-system-tools.desktop

# Remove config
rm -rf ~/.config/allinone-system-tools

# Remove PATH entry (manually edit ~/.bashrc or ~/.zshrc)
```

## 📦 Development Installation

For contributors and developers:

```bash
# Clone repository
git clone https://github.com/Srijan-XI/AIO-SDMS.git
cd aio-sdms

# Install in development mode
python3 -m venv venv
source venv/bin/activate
pip install -e .
pip install -r requirements-linux.txt
pip install pytest pytest-cov black isort

# Run tests
pytest tests/

# Format code
black .
isort .
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests and ensure code quality
5. Submit a pull request

## 📄 License & Support

This project is licensed under the MIT License. See the `LICENSE` file for details.

Support channels:
- GitHub Issues: https://github.com/Srijan-XI/AIO-SDMS/issues
- Documentation: https://github.com/Srijan-XI/AIO-SDMS/wiki
- Discussions: https://github.com/Srijan-XI/AIO-SDMS/discussions

---

## ✅ Summary

This combined document consolidates the detailed installation steps from `INSTALL_LINUX.md` and the setup summary from `LINUX_SETUP.md`. Use this file as a single canonical reference for Linux installation, setup, verification, troubleshooting, development and uninstallation.

If you want, I can also:
- Replace the original two files with this single file (delete the originals and update any links).
- Add a short top-level README note pointing Linux users to this combined file.
