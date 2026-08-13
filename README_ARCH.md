# CachyOS & Arch Linux Setup Guide

This guide provides a comprehensive, post-install setup walkthrough for Arch Linux, optimized specifically for **CachyOS**. The configuration and packages included here are tailored to match modern development requirements, custom hardware tuning, and robust BTRFS-based recovery systems.

---

## 🚀 System Updates & Repositories

### 1. Perform a Full System Upgrade
Keep your system packages up to date with `pacman`:
```bash
sudo pacman -Syu
```

### 2. Configure Chaotic-AUR (Optional/Recommended)
Chaotic-AUR is a repository for Arch Linux providing precompiled AUR packages, saving substantial compilation time for large packages.

To initialize keys and add the repository:
```bash
# Retrieve keys
sudo pacman-key --recv-key 3056513887B78AEB --keyserver keyserver.ubuntu.com
sudo pacman-key --lsign-key 3056513887B78AEB

# Install keyrings and mirrorlist
sudo pacman -U 'https://cdn-mirror.chaotic.cx/chaotic-aur/chaotic-keyring.pkg.tar.zst'
sudo pacman -U 'https://cdn-mirror.chaotic.cx/chaotic-aur/chaotic-mirrorlist.pkg.tar.zst'
```

Add the following sections to your `/etc/pacman.conf` using your favorite text editor (e.g., `sudo nvim /etc/pacman.conf`):
```ini
[chaotic-aur]
Include = /etc/pacman.d/chaotic-mirrorlist
```
*After saving, sync your database:*
```bash
sudo pacman -Syyu
```

---

## 🛡️ BTRFS, LUKS Encryption & System Recovery

The system uses LUKS full-disk encryption on top of BTRFS with separate subvolumes (`@`, `@home`, `@root`, `@srv`, `@cache`, `@log`, `@tmp`). Automatic snapshots are managed by **Snapper** with Limine boot-menu integration — not Timeshift/GRUB.

### 1. Install Snapper & Limine Integration
CachyOS provides helper packages that wire everything together:
```bash
sudo pacman -S snapper btrfs-progs btrfs-assistant \
  limine limine-snapper-sync cachyos-snapper-support
```

### 2. Verify Snapper Configuration
```bash
snapper list-configs
snapper list
```

### 3. BTRFS Assistant (GUI Manager)
For managing BTRFS subvolumes, Snapper configs, and snapshots via a GUI:
```bash
btrfs-assistant
```

### 4. LUKS Layout Reference
```
nvme0n1p1  →  /boot   (vfat, EFI)
nvme0n1p2  →  LUKS    (btrfs)
  ├─ @       →  /
  ├─ @home   →  /home
  ├─ @root   →  /root
  ├─ @srv    →  /srv
  ├─ @cache  →  /var/cache
  ├─ @log    →  /var/log
  └─ @tmp    →  /var/tmp
zram0      →  [SWAP]
```

---

## 🎮 NVIDIA Graphics & Container Toolkit

### 1. NVIDIA Open Kernel Modules (CachyOS)
On CachyOS, the recommended approach is the prebuilt open-kernel-module package that tracks the CachyOS kernel:
```bash
sudo pacman -S linux-cachyos-nvidia-open nvidia-utils lib32-nvidia-utils nvidia-settings
```
*This replaces the manual `nvidia-dkms` approach — the open modules are rebuilt automatically with each kernel update.*

### 2. Hybrid Graphics / Optimus (RTX 2000 Ada + Intel Arc)
This laptop uses hybrid graphics. Install `nvidia-prime` and enable `switcheroo-control` for runtime GPU switching:
```bash
sudo pacman -S nvidia-prime switcheroo-control
sudo systemctl enable --now switcheroo-control
```
*Usage:* Run `prime-run <command>` (e.g., `prime-run steam`).

### 3. NVIDIA Container Toolkit (Docker GPU Integration)
To enable GPU-accelerated container workflows:
```bash
sudo pacman -S nvidia-container-toolkit
```

---

## ⚙️ Power Management, Key Remapping & Tuning

### 1. CPU Power & Hybrid Graphics
```bash
# Install CPU power management
sudo pacman -S cpupower

# Disable power-profiles-daemon to prevent conflicts with cpupower
sudo systemctl disable --now power-profiles-daemon

# Enable cpupower
sudo systemctl enable --now cpupower.service
```

### 2. Keyd Key Remapping
`keyd` is an extremely low-overhead system-level key remapping daemon.

```bash
sudo pacman -S keyd
sudo systemctl enable --now keyd
```

*Configure keymappings at `/etc/keyd/default.conf`. Current Copilot key mapping:*
```ini
[ids]
*

[main]
# Map the Copilot key chord to Right Control
leftmeta+leftshift+f23 = rightcontrol
```
Reload config:
```bash
sudo systemctl restart keyd
```

#### Finding the Copilot Key Scan Code
1. Run `sudo keyd monitor` (or `sudo evtest`) and press the Copilot key.
2. Note the emitted combination (e.g., `leftmeta+leftshift+f23`).
3. Add the mapping to `/etc/keyd/default.conf` and restart keyd.

To restrict remapping to the built-in laptop keyboard only, replace `*` in `[ids]` with the hardware ID from `keyd monitor` (e.g., `0001:0001`).

### 3. SSD Trim Activation
```bash
sudo systemctl enable --now fstrim.timer
```

### 4. Firewall (UFW)
```bash
sudo pacman -S ufw ufw-extras
sudo systemctl enable --now ufw
sudo ufw enable
```

---

## 📦 Essential System Packages

### 1. Core Development, Archives & CLI Tools
```bash
sudo pacman -S --needed base-devel git python-pip cmake qt6-tools gcc gdb \
unzip zip p7zip unrar tar lrzip xclip meld curl wget extra-cmake-modules \
mesa ninja libtool autoconf automake pkgconf zsh python-virtualenv mc \
fastfetch ripgrep fd aria2 bat neovim ranger trash-cli hwatch tree \
xarchiver ntfsfix ntfs-3g openconnect gtk-engine-murrine \
copyq evince satty grim slurp libsecret nodejs npm git-lfs \
vulkan-devel cronie starship
```

*Start cron scheduler:*
```bash
sudo systemctl enable --now cronie.service
```

### 2. AUR Helper Setup (`paru`)
CachyOS ships with `paru` preinstalled. If you need to bootstrap it manually:
```bash
git clone https://aur.archlinux.org/paru.git
cd paru
makepkg -si
```

---

## 🐚 Terminal Enhancements

### 1. CachyOS Zsh Config & Starship Prompt
CachyOS provides a preconfigured zsh environment via `cachyos-zsh-config` (includes Oh My Zsh, fzf, and sensible defaults). Pair it with **Starship** for a fast, customizable prompt:
```bash
sudo pacman -S cachyos-zsh-config starship
```

Ensure your `~/.zshrc` sources the CachyOS config:
```bash
source /usr/share/cachyos-zsh-config/cachyos-config.zsh
eval "$(starship init zsh)"
```

A custom Starship config is available in this repo at [`config/starship.toml`](config/starship.toml).

### 2. Atuin (Fuzzy Shell History Search)
Install Atuin for modern, SQLite-backed shell history search:
```bash
# Install via official script (or: sudo pacman -S atuin)
curl --proto '=https' --tlsv1.2 -LsSf https://setup.atuin.sh | sh

# Import existing zsh history
atuin import auto

# Initialize for zsh
echo 'eval "$(atuin init zsh)"' >> ~/.zshrc
```

### 3. Zoxide, UV, & Zellij
```bash
# Directory jumper and terminal multiplexer
sudo pacman -S zoxide zellij

# Initialize zoxide in ~/.zshrc
echo 'eval "$(zoxide init zsh --cmd cd)"' >> ~/.zshrc

# Install uv (blazing-fast Python package/project manager)
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Run an MCP proxy from your named server config when you need a stateless HTTP endpoint:
```bash
uvx mcp-proxy --named-server-config ~/.mcp.json --allow-origin "*" --port 8001 --stateless
```

### 4. Terminal Emulators
Currently installed terminals:
- **Ghostty** (primary): `sudo pacman -S ghostty`
- **Kitty**: `sudo pacman -S kitty`
- **Alacritty**: `sudo pacman -S alacritty`

#### Ghostty Custom Configuration (`~/.config/ghostty/config`):
```ini
# Fonts
font-family = "Maple Mono NF"
font-size = 10

# Custom shader (optional)
custom-shader = /home/sonul/Documents/github/ghostty-shaders/smear_cursor_blocks.glsl
```

Kitty theme configs are available in this repo at [`config/kitty/`](config/kitty/).

### 5. Yazi Terminal File Manager
```bash
sudo pacman -S yazi ffmpeg 7zip jq poppler fd ripgrep fzf zoxide resvg imagemagick
```

---

## 🎨 Desktop Environment (KDE Plasma 6)

### 1. Core KDE Packages
CachyOS ships a full Plasma 6 desktop. Key packages already in use:
```bash
sudo pacman -S plasma-desktop konsole dolphin kate spectacle copyq \
  kdeconnect powerdevil kde-gtk-config plasma-browser-integration
```

CachyOS-specific KDE theming and settings:
```bash
sudo pacman -S cachyos-kde-settings cachyos-iridescent-kde \
  cachyos-nord-kde-theme-git cachyos-emerald-kde-theme-git
```

### 2. Recommended KDE Tools
```bash
sudo pacman -S ark gwenview haruna filelight partitionmanager \
  kcalc kwalletmanager kinfocenter kscreen meld
```

### 3. Material You Colors (Dynamic Theming)
Generates Material You color schemes from your wallpaper and applies them across the Plasma desktop.

```bash
paru -S kde-material-you-colors
```

#### Light Mode
Apply a light Material You theme from the current wallpaper:
```bash
kde-material-you-colors --light
```

To switch to dark mode instead:
```bash
kde-material-you-colors --dark
```

#### Autostart on Login
Enable automatic theming at KDE startup (runs after the panel loads):
```bash
kde-material-you-colors --light --autostart
```

This copies a desktop entry to `~/.config/autostart/`. To use light mode, ensure the `Exec` line reads:
```ini
Exec=kde-material-you-colors --light
```

Or create/edit `~/.config/autostart/kde-material-you-colors.desktop` manually:
```ini
[Desktop Entry]
Exec=kde-material-you-colors --light
Name=kde-material-you-colors
Type=Application
Terminal=False
X-KDE-autostart-after=panel
```

#### Optional Configuration
Copy the default config file for persistent settings (scheme variant, pywal integration, opacity, etc.):
```bash
kde-material-you-colors --copyconfig
```
Edit `~/.config/kde-material-you-colors/config.conf` to customize. CLI flags like `--light` override values in the config file.

---

## 💻 Development Tools, Editors & Browsers

### 1. Editors & IDEs
- **Neovim (LazyVim Starter)**:
  ```bash
  git clone https://github.com/LazyVim/starter ~/.config/nvim
  rm -rf ~/.config/nvim/.git
  ```
  Neovim plugin configs are in this repo at [`config/nvim/`](config/nvim/).
- **Visual Studio Code**: `paru -S visual-studio-code-bin`
- **Cursor IDE**: `paru -S cursor-bin`
- **Fresh Editor**: `paru -S fresh-editor-bin`

### 2. Web Browsers
```bash
paru -S brave-bin vivaldi microsoft-edge-stable-bin
```

### 3. Perforce (Game Dev)
```bash
sudo pacman -S p4 p4v
```

---

## 🎞️ Multimedia & Productivity Apps

### 1. Media Engines & Codecs
```bash
sudo pacman -S gst-plugins-good gst-plugins-bad gst-plugins-ugly gst-libav
```

### 2. Multimedia Tools
```bash
sudo pacman -S vlc gimp ffmpeg obs-studio haruna
```

### 3. Productivity & Utilities
- **OnlyOffice Suite**: `paru -S onlyoffice-bin`
- **Draw.io Desktop**: `paru -S drawio-desktop`
- **CopyQ** (clipboard manager): `sudo pacman -S copyq`
- **Glances** (system monitor): `sudo pacman -S glances`
- **Gufw** (UFW GUI): `sudo pacman -S gufw`

### 4. Flatpak Apps
```bash
sudo pacman -S flatpak
flatpak remote-add --if-not-exists flathub https://flathub.org/repo/flathub.flatpakrepo

# Installed flatpaks
flatpak install flathub net.cozic.joplin_desktop    # Joplin notes
flatpak install flathub net.meshlab.MeshLab          # MeshLab 3D
flatpak install flathub org.gnome.gitlab.YaLTeR.VideoTrimmer
flatpak install flathub com.github.tchx84.Flatseal   # Flatpak permissions manager
```

---

## 🐳 Virtualization & Containers

### 1. Docker
```bash
sudo pacman -S docker docker-compose
sudo systemctl enable --now docker
sudo usermod -aG docker $USER
```

### 2. Distrobox
Create and run containerized Linux distributions with zero overhead and full desktop integration:
```bash
sudo pacman -S distrobox
```

### 3. Rootless Podman Setup (Alternative)
See the [`install_podman.sh`](install_podman.sh) script in this repository for a rootless Podman setup.

---

## ⚙️ Optional / Advanced Configurations

### 1. ZRam Swapping
CachyOS enables zram swap by default (~50% of RAM, zstd compression). Verify with:
```bash
zramctl
```
No manual `systemd-zram-generator` configuration is needed on a stock CachyOS install.

### 2. Bluetooth Stack
```bash
sudo pacman -S bluez bluez-utils
sudo systemctl enable --now bluetooth.service
```

---

## 📚 General Arch Resources
* Consult the [Arch Wiki](https://wiki.archlinux.org/) (the gold standard of Linux documentation).
* Browse the [CachyOS Wiki](https://wiki.cachyos.org/) for kernel optimizations and optimized compiler flag details.
