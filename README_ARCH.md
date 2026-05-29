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

## 🛡️ BTRFS, System Recovery & Backups

For systems running on a BTRFS filesystem, this setup integrates automatic system recovery points using Timeshift, automatically generating GRUB boot entries for snapshots before any system update.

### 1. Install Timeshift & Snapping Hooks
```bash
# Install core utilities from official repositories
sudo pacman -S timeshift

# Install snapshot hooks and GRUB integration from AUR
yay -S timeshift-autosnap grub-btrfs
```

### 2. Configure Automatic GRUB Menu Generation
To automatically append Timeshift backup points to your GRUB boot options upon system upgrades, enable the `grub-btrfsd` systemd service:

1. Edit the service unit to listen specifically to Timeshift changes:
   ```bash
   sudo systemctl edit --full grub-btrfsd
   ```
2. Modify the `ExecStart` line to include the `--timeshift-auto` flag:
   ```ini
   ExecStart=/usr/bin/grub-btrfsd --syslog --timeshift-auto
   ```
3. Reload `systemd`, then enable and start the daemon:
   ```bash
   sudo systemctl daemon-reload
   sudo systemctl enable --now grub-btrfsd
   ```

### 3. BTRFS Assistant (GUI Manager)
For managing BTRFS subvolumes, Snapper configs, and Timeshift backups via a premium GUI, you can launch:
```bash
btrfs-assistant-launcher
```

---

## 🎮 NVIDIA Graphics & Container Toolkit

### 1. Proprietary NVIDIA DKMS Drivers
For machines utilizing NVIDIA graphics cards, install the DKMS-enabled drivers so they update automatically along with kernel changes:
```bash
sudo pacman -S nvidia-dkms nvidia-utils lib32-nvidia-utils nvidia-settings
```

### 2. Hybrid Graphics / Optimus Switcher
If you are on an Optimus/hybrid graphics laptop, install `nvidia-prime` to run heavy tasks on the discrete GPU:
```bash
yay -S nvidia-prime prime-run
```
*Usage:* Run `prime-run <command>` (e.g., `prime-run steam`).

### 3. NVIDIA Container Toolkit (Docker/Podman Integration)
To enable GPU-accelerated container workflows:
```bash
sudo pacman -S nvidia-container-toolkit
```

---

## ⚙️ Power Management, Key Remapping & Tuning

### 1. Thermal & Performance Optimization
CachyOS is optimized for performance, but you can configure hardware-specific power-saving/tuning daemons to manage CPU states dynamically:
```bash
# Install CPU power & thermald
sudo pacman -S cpupower thermald

# Disable the standard power-profiles-daemon to prevent conflicts
sudo systemctl disable --now power-profiles-daemon

# Enable and start optimized services
sudo systemctl enable --now cpupower.service
sudo systemctl enable --now thermald
```

### 2. Keyd Key Remapping
`keyd` is an extremely low-overhead system-level key remapping daemon.

```bash
# Install keyd from official repos
sudo pacman -S keyd

# Enable and start keyd service
sudo systemctl enable --now keyd
```

*Configure keymappings at `/etc/keyd/default.conf`. For example:*
```ini
[ids]
*

[main]
# Map capslock to escape when pressed, or control when held
capslock = overload(control, esc)
```
Reload config:
```bash
sudo systemctl restart keyd
```

#### Custom Mapping: Copilot Key to Right Ctrl / Compose
Modern laptops with a Copilot key don't emit a single scan code. Instead, the firmware sends a keyboard chord, typically `leftmeta + leftshift + f23` or `leftmeta + leftshift`. We can use `keyd` to capture and remap this combination.

1. **Find what the Copilot key emits**:
   Run:
   ```bash
   sudo keyd monitor
   # or
   sudo evtest
   ```
   Press the Copilot key and look for the emitted combination (e.g., `leftmeta+leftshift+f23`).

2. **Add the mapping to `/etc/keyd/default.conf`**:
   ```ini
   [ids]
   *

   [main]
   # Map the Copilot key chord to Right Control
   leftmeta+leftshift+f23 = rightcontrol

   # If your firmware sends f23 sequentially rather than as a chord, map f23 alone:
   # f23 = rightcontrol

   # Alternatively, restore the classic Menu/Compose behavior:
   # f23 = compose
   # f23 = menu
   ```

3. **Restrict to the Laptop Keyboard only (Optional)**:
   To prevent external keyboards from being affected, run `keyd monitor` to identify your built-in keyboard's hardware ID (e.g., `0001:0001`) and target only that device in the config:
   ```ini
   [ids]
   0001:0001  # Replace with your laptop keyboard ID

   [main]
   leftmeta+leftshift+f23 = rightcontrol
   ```

4. **Reload keyd**:
   ```bash
   sudo systemctl restart keyd
   ```


### 3. SSD Trim Activation
Enable standard automatic solid-state drive cell optimization:
```bash
sudo systemctl enable --now fstrim.timer
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
copyq evince gnome-text-editor loupe gnome-calculator flameshot \
libsecret nodejs npm git-lfs pwvucontrol vulkan-devel cronie
```

*Start cron scheduler:*
```bash
sudo systemctl enable --now cronie.service
```

### 2. AUR Helper Setup (`yay` or `paru`)
If you do not have an AUR helper installed, compile and bootstrap `yay` directly from source:
```bash
git clone https://aur.archlinux.org/yay.git
cd yay
makepkg -si
```

---

## 🐚 Terminal Enhancements

### 1. Oh My Zsh & Custom Plugins
Install Oh My Zsh:
```bash
sh -c "$(curl -fsSL https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)"
```

Clone highly recommended productivity plugins:
```bash
# Zsh Autosuggestions
git clone https://github.com/zsh-users/zsh-autosuggestions ${ZSH_CUSTOM:-~/.oh-my-zsh/custom}/plugins/zsh-autosuggestions

# Zsh Syntax Highlighting
git clone https://github.com/zsh-users/zsh-syntax-highlighting.git ${ZSH_CUSTOM:-~/.oh-my-zsh/custom}/plugins/zsh-syntax-highlighting

# Zsh You-Should-Use (reminds you of aliases)
git clone https://github.com/MichaelAquilina/zsh-you-should-use.git $ZSH_CUSTOM/plugins/you-should-use

# Safe RM (prevent accidental data loss)
git clone --recursive --depth 1 https://github.com/mattmc3/zsh-safe-rm.git ${ZSH_CUSTOM:-~/.oh-my-zsh/custom}/plugins/zsh-safe-rm
```

Update the plugin activation array in your `~/.zshrc`:
```bash
sed -i 's/^plugins=(git)/plugins=(git zsh-autosuggestions zsh-syntax-highlighting you-should-use zsh-safe-rm emoji emotty)/' ~/.zshrc
```

### 2. Atuin (Fuzzy Shell History Search)
Install and initialize Atuin for modern, SQLite-backed shell history search:
```bash
# Install via pacman
sudo pacman -S atuin

# Import existing zsh history into Atuin
atuin import auto

# Initialize for zsh
echo 'eval "$(atuin init zsh)"' >> ~/.zshrc
```

### 3. Zoxide, UV, & Zellij
```bash
# Install zoxide directory jumper and zellij multiplexer
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

This is useful for exposing MCP servers to local tools or web clients that expect HTTP transport. Adjust the config path, port, or origin policy as needed.

### 4. Modern Terminal Emulators
- **Wezterm**: `sudo pacman -S wezterm`
- **Kitty**: `sudo pacman -S kitty`
- **Ghostty**: Install the ultimate high-performance terminal emulator from AUR:
  ```bash
  yay -S ghostty
  ```

#### Ghostty Custom Configuration (`~/.config/ghostty/config`):
```ini
font-family = "MonoLisa Nerd Font"
font-size = 10
gtk-titlebar = true
window-decoration = true
gtk-tabs-location = top
freetype-load-flags = no-hinting
gtk-titlebar-style = tabs
theme = Catppuccin Mocha

# === Cursor Settings ===
cursor-style = block
cursor-style-blink = false
cursor-click-to-move = true

# === Shell Integration ===
shell-integration = detect
shell-integration-features = cursor,sudo,title

# === Quick Terminal (Dropdown / Overlay) ===
quick-terminal-screen = main
quick-terminal-position = top
quick-terminal-size = 40%,100%
quick-terminal-animation-duration = 0.2

# === Misc Settings ===
clipboard-read = allow
clipboard-write = allow
clipboard-paste-protection = true
clipboard-paste-bracketed-safe = true
```

#### Nemo File Manager Integration:
To open Ghostty directly from the Nemo context menu inside the current directory:
```bash
gsettings set org.cinnamon.desktop.default-applications.terminal exec 'ghostty --working-directory=%P'
```

### 5. Yazi Terminal File Manager
Yazi is an asynchronous Rust terminal file manager. Install Yazi along with its extensive suite of optional preview/compression engines:
```bash
sudo pacman -S yazi ffmpeg 7zip jq poppler fd ripgrep fzf zoxide resvg imagemagick
```

---

## 🎨 Desktop Environment (GNOME & Styling)

### 1. Essential GNOME Tools & Frameworks
Ensure your GNOME environment supports custom layouts, extensions, and styling hooks:
```bash
sudo pacman -S gnome-tweaks extension-manager gnome-browser-connector gnome-themes-extra
```

### 2. Premium Themes & Icon Packs
Install the user-preferred visual assets:
```bash
# Official packages
sudo pacman -S papirus-icon-theme morewaita-icon-theme

# AUR packages
yay -S bibata-cursor-theme-bin graphite-gtk-theme graphite-gtk-theme-wallpaper
yay -S mint-themes mint-y-icons mint-x-icons mint-backgrounds mint-sounds
```

### 3. GNOME Advanced Configuration Tweaks
Run these GSettings commands to tailor system behavior:
```bash
# Center all newly spawned application windows
gsettings set org.gnome.mutter center-new-windows true

# Enable desktop dash click action to minimize active windows
# (Note: Requires Dash-to-Dock or Dash-to-Panel extensions enabled)
gsettings set org.gnome.shell.extensions.dash-to-dock click-action 'minimize'

# Open folders automatically on drag-and-drop hover in Nautilus
gsettings set org.gnome.nautilus.preferences open-folder-on-dnd-hover true

# Overamplify volume slider (Allow volume level above 100%)
gsettings set org.gnome.desktop.sound allow-volume-above-100-percent true

# Enable high-density multi-monitor Fractional Scaling (Wayland)
gsettings set org.gnome.mutter experimental-features "['scale-monitor-framebuffer']"
```

---

## 💻 Development Tools, Editors & Browsers

### 1. Editors & IDEs
- **Neovim (LazyVim Starter)**:
  ```bash
  git clone https://github.com/LazyVim/starter ~/.config/nvim
  rm -rf ~/.config/nvim/.git
  ```
- **Visual Studio Code**: `sudo pacman -S visual-studio-code-bin` or AUR `visual-studio-code-insiders-bin`
- **Cursor IDE**: Install the AI code editor:
  ```bash
  yay -S cursor-bin
  ```

### 2. Modern Web Browsers
```bash
yay -S google-chrome zen-browser-bin microsoft-edge-stable-bin
```

---

## 🎞️ Multimedia & Productivity Apps

### 1. Media Engines & Codecs
To ensure smooth playbacks and encoding capabilities across all applications:
```bash
sudo pacman -S gst-plugins-good gst-plugins-bad gst-plugins-ugly gst-libav
```

### 2. Multimedia Tools
```bash
# Official repositories
sudo pacman -S vlc gimp ffmpeg nomacs mpv obs-studio

# AUR / Specialized tools
yay -S krita blender bulky
```

### 3. Productivity & Whiteboarding
- **OnlyOffice Suite**: `yay -S onlyoffice-bin`
- **Spacedrive (File Manager)**: `yay -S spacedrive-bin`
- **MarkText (Markdown Editor)**: `paru -S MarkText` or `yay -S marktext-bin`
- **LM Studio (Local LLMs)**: `paru -S lmstudio-bin`
- **Beyond Compare (Diff/Merge)**: `paru -S bcompare`
- **RenderDoc (Graphics Debugger)**: `paru -S renderdoc`

---

## 🐳 Virtualization & Containers

### 1. Distrobox
Create and run containerized Linux distributions with zero overhead and full desktop integration:
```bash
sudo pacman -S distrobox
```

### 2. Rootless Podman Setup
Arch offers natively optimized rootless Podman setup, avoiding manual compile scripts:
```bash
# Install Podman
sudo pacman -S podman

# Enable support for user namespaces & rootless execution
if [ ! -e /etc/subuid ] || [ ! -e /etc/subgid ]; then
    sudo pacman -S shadow  # Ensures newuidmap/newgidmap are available
    echo "$(whoami):100000:65536" | sudo tee /etc/subuid | sudo tee /etc/subgid
fi

# Run migrate to configure container backend
podman system migrate
```

---

## ⚙️ Optional / Advanced Configurations

### 1. Flatpak Setup
```bash
sudo pacman -S flatpak
flatpak remote-add --if-not-exists flathub https://flathub.org/repo/flathub.flatpakrepo
```

### 2. Snap Packages Support
```bash
# Install snap daemon
sudo pacman -S snapd
sudo systemctl enable --now snapd.socket

# Add classic symbolic link integration
sudo ln -s /var/lib/snapd/snap /snap
```

### 3. ZRam Swapping optimization via Generator
Arch natively features `systemd-zram-generator` for low-overhead dynamic RAM swaps:
1. Install generator:
   ```bash
   sudo pacman -S systemd-zram-generator
   ```
2. Create configuration file `/etc/systemd/zram-generator.conf`:
   ```ini
   [zram0]
   zram-size = ram / 2
   ```
3. Load dynamic swapping block:
   ```bash
   sudo systemctl daemon-reload
   sudo systemctl start systemd-zram-setup@zram0.service
   ```

### 4. Bluetooth Stack
```bash
sudo pacman -S bluez bluez-utils
sudo systemctl enable --now bluetooth.service
```

---

## 📚 General Arch Resources
* Consult the [Arch Wiki](https://wiki.archlinux.org/) (the gold standard of Linux documentation).
* Browse the [CachyOS Wiki](https://wiki.cachyos.org/) for kernel optimizations and optimized compiler flag details.
