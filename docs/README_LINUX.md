# 🐧 Linux Setup - All-in-One System Tools

## Quick Installation

```bash
# 1. Clone the repository
git clone https://github.com/Srijan-XI/AIO-SDMS.git
cd aio-sdms

# 2. Make setup script executable
chmod +x setup.sh

# 3. Run the automatic setup
./setup.sh
```

## What the Setup Script Does

✅ **System Dependencies**: Installs required libraries (audio, video, bluetooth, etc.)  
✅ **Python Environment**: Creates isolated virtual environment  
✅ **Package Installation**: Installs all Python dependencies  
✅ **Launcher Creation**: Creates `allinone-tools` command  
✅ **Desktop Integration**: Adds application to system menu  
✅ **Permissions Setup**: Configures hardware access permissions  
✅ **PATH Configuration**: Updates shell configuration files  

## Usage After Installation

```bash
# Command Line Interface (default)
allinone-tools

# Specific tools
allinone-tools battery      # Battery monitoring
allinone-tools diagnostics  # Hardware diagnostics  
allinone-tools monitor      # System monitoring
allinone-tools packages     # Package management

# Web Interface
allinone-tools --web        # Launch web interface
# Then open: http://localhost:5000

# Help and options
allinone-tools --help       # Show all options
```

## Supported Linux Distributions

| Distribution | Status | Package Manager |
|-------------|--------|----------------|
| Ubuntu 20.04+ | ✅ Fully Supported | `apt` |
| Debian 11+ | ✅ Fully Supported | `apt` |
| Fedora 36+ | ✅ Fully Supported | `dnf` |
| CentOS 8+ | ✅ Fully Supported | `dnf/yum` |
| Arch Linux | ✅ Fully Supported | `pacman` |
| Manjaro | ✅ Fully Supported | `pacman` |
| openSUSE | ⚠️ Should Work | `zypper` |
| Linux Mint | ⚠️ Should Work | `apt` |

## Manual Installation (If Automatic Fails)

<details>
<summary>Click to expand manual installation steps</summary>

### 1. Install System Dependencies

**Ubuntu/Debian:**
```bash
sudo apt-get update
sudo apt-get install -y python3-dev python3-venv python3-pip build-essential \
    portaudio19-dev libasound2-dev libsdl2-dev libsdl2-mixer-dev \
    libopencv-dev python3-opencv bluetooth libbluetooth-dev bluez bluez-tools
```

**Fedora/CentOS:**
```bash
sudo dnf install -y python3-devel gcc gcc-c++ make portaudio-devel \
    alsa-lib-devel SDL2-devel SDL2_mixer-devel opencv-devel \
    python3-opencv bluez bluez-libs-devel
```

**Arch Linux:**
```bash
sudo pacman -S python python-pip base-devel portaudio alsa-lib \
    sdl2 sdl2_mixer opencv python-opencv bluez bluez-utils
```

### 2. Create Installation Directory
```bash
mkdir -p ~/.local/share/allinone-system-tools
cp -r * ~/.local/share/allinone-system-tools/
cd ~/.local/share/allinone-system-tools
```

### 3. Setup Python Environment
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements-linux.txt
```

### 4. Create Launcher
```bash
mkdir -p ~/.local/bin
cat > ~/.local/bin/allinone-tools << 'EOF'
#!/bin/bash
source ~/.local/share/allinone-system-tools/venv/bin/activate
cd ~/.local/share/allinone-system-tools
python main.py "$@"
deactivate
EOF
chmod +x ~/.local/bin/allinone-tools
```

### 5. Update PATH
```bash
echo 'export PATH="$PATH:$HOME/.local/bin"' >> ~/.bashrc
source ~/.bashrc
```

</details>

## Troubleshooting

### Permission Issues
```bash
# Add user to required groups
sudo usermod -a -G audio,video,dialout $USER
# Log out and back in
```

### Audio Issues
```bash
# Check audio system
pulseaudio --check -v
# Restart if needed
pulseaudio -k && pulseaudio --start
```

### Camera Issues
```bash
# Check camera access
ls -l /dev/video*
# Install camera tools
sudo apt-get install v4l-utils
v4l2-ctl --list-devices
```

### Python Environment Issues
```bash
# Recreate virtual environment
rm -rf ~/.local/share/allinone-system-tools/venv
cd ~/.local/share/allinone-system-tools
python3 -m venv venv
source venv/bin/activate
pip install -r requirements-linux.txt
```

## Verification

Test your installation:
```bash
cd ~/.local/share/allinone-system-tools
python3 verify_installation.py
```

## Uninstallation

```bash
# Automatic uninstall
~/.local/share/allinone-system-tools/uninstall.sh

# Manual cleanup
rm -rf ~/.local/share/allinone-system-tools
rm -f ~/.local/bin/allinone-tools
rm -f ~/.local/share/applications/allinone-system-tools.desktop
rm -rf ~/.config/allinone-system-tools
```

## File Locations

- **Installation**: `~/.local/share/allinone-system-tools/`
- **Launcher**: `~/.local/bin/allinone-tools`
- **Config**: `~/.config/allinone-system-tools/`
- **Desktop Entry**: `~/.local/share/applications/allinone-system-tools.desktop`
- **Logs**: `~/.local/share/allinone-system-tools/logs/`

# Getting Help

- 📖 **Full Guide**: `docs/I&S_LINUX.md`
- 🐛 **Issues**: [GitHub Issues](https://github.com/Srijan-XI/AIO-SDMS/issues)
- 💬 **Discussions**: [GitHub Discussions](https://github.com/Srijan-XI/AIO-SDMS/discussions)

---

**Need Windows installation?** See the main `README.md` file.