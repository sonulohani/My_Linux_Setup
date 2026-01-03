# Arch Linux Setup Guide

This guide provides instructions for setting up an Arch Linux system with essential tools and configurations, mirroring the setup in the Ubuntu guide. Use `pacman` for official packages and an AUR helper (like `yay` or `paru`) for AUR packages.

**Note:** Package names might differ slightly. Always verify with `pacman -Ss <search-term>` or search the AUR.

## System Updates

Keep your system up-to-date:
```bash
sudo pacman -Syu
```

## Essential Packages & Setup

### Core Development & System Tools
Install essential tools for development and system management:
```bash
# Core build tools and utilities
sudo pacman -S base-devel git python-pip cmake qt6-tools gcc gdb unrar p7zip htop xclip meld curl wget extra-cmake-modules mesa ninja libtool autoconf automake pkgconf unzip ttf-hack zsh python-virtualenv mc \
lazygit fastfetch ripgrep fd aria2 bat neovim ranger trash-cli hwatch

# Optional but recommended
# sudo pacman -S preload # Check AUR if not in official repos - preload often causes issues, consider removing or keeping commented

# Fonts (DejaVu included in ttf-dejavu, often installed by default or as dependency)
sudo pacman -S ttf-dejavu
```
*Note: `build-essential` on Ubuntu is roughly equivalent to the `base-devel` group on Arch.*

### Enable Firewall (ufw)
Install `ufw` if needed and enable it:
```bash
sudo pacman -S ufw
sudo systemctl enable ufw.service && sudo systemctl start ufw.service
sudo ufw enable
```

### Enable SSD Trim (fstrim.timer)
```bash
sudo systemctl enable fstrim.timer && sudo systemctl start fstrim.timer
```

### Flatpak Setup
Install Flatpak and configure the Flathub repository:
```bash
sudo pacman -S flatpak
flatpak remote-add --if-not-exists flathub https://flathub.org/repo/flathub.flatpakrepo
```

### Git Configuration
Set your Git username and email, and configure Meld as the merge/diff tool:
```bash
git config --global user.name "Sonu Lohani"
git config --global user.email "sonulohani@gmail.com"
git config --global merge.tool meld
git config --global diff.tool meld
```

## Terminal Enhancements

### Wezterm Terminal
Install Wezterm (check official repos first, then AUR):
```bash
sudo pacman -S wezterm
# or using an AUR helper: yay -S wezterm-git
```
[Wezterm Installation Docs](https://wezfurlong.org/wezterm/install/linux.html#installing-on-arch-linux)

### Oh My Zsh & Plugins
Install Zsh first if you haven't:
```bash
sudo pacman -S zsh
```
Install Oh My Zsh:
```bash
sh -c "$(curl -fsSL https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)"
```
Install Zsh plugins (same commands as Ubuntu):
```bash
# Autosuggestions
git clone https://github.com/zsh-users/zsh-autosuggestions ${ZSH_CUSTOM:-~/.oh-my-zsh/custom}/plugins/zsh-autosuggestions
# Syntax Highlighting
git clone https://github.com/zsh-users/zsh-syntax-highlighting.git ${ZSH_CUSTOM:-~/.oh-my-zsh/custom}/plugins/zsh-syntax-highlighting
# You Should Use
git clone https://github.com/MichaelAquilina/zsh-you-should-use.git $ZSH_CUSTOM/plugins/you-should-use
# Safe RM
git clone --recursive --depth 1 https://github.com/mattmc3/zsh-safe-rm.git ${ZSH_CUSTOM:-~/.oh-my-zsh/custom}/plugins/zsh-safe-rm
```
Enable plugins in `~/.zshrc` (same command as Ubuntu):
```bash
sed -i 's/^plugins=(git)/plugins=(git zsh-autosuggestions zsh-syntax-highlighting you-should-use zsh-safe-rm emoji emotty)/' ~/.zshrc
```
*Remember to source your `~/.zshrc` or restart your shell after modifying it.*

### Atuin Shell History
Install Atuin (check official repos first, then AUR):
```bash
sudo pacman -S atuin
# or using an AUR helper: yay -S atuin
```

### uv
Install uv:
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### Zellij Terminal Multiplexer
Install Zellij (check official repos first, then AUR):
```bash
sudo pacman -S zellij
# or using an AUR helper: yay -S zellij
```
[Zellij Website](https://zellij.dev/)

### Kitty Terminal
Install Kitty terminal emulator:
```bash
sudo pacman -S kitty
```
[Kitty Terminfo Fix](https://sw.kovidgoyal.net/kitty/faq/#i-get-errors-about-the-terminal-being-unknown-or-opening-the-terminal-failing-or-functional-keys-like-arrow-keys-don-t-work)

### Yazi Terminal File Manager
Yazi is a blazing-fast terminal file manager written in Rust. Install it and recommended optional dependencies:

```bash
# Official Arch package
sudo pacman -S yazi ffmpeg 7zip jq poppler fd ripgrep fzf zoxide resvg imagemagick
```

Documentation: https://yazi-rs.github.io/docs/installation
Repository: https://github.com/sxyazi/yazi

## Desktop Environment (GNOME)

### Essential GNOME Packages & Tweaks
Install Tweaks tool and Extension support:
```bash
sudo pacman -S gnome-tweaks gnome-shell-extensions
```
Apply GNOME settings tweaks (same commands as Ubuntu):
```bash
# Center new windows
gsettings set org.gnome.mutter center-new-windows true
# Set dash-to-dock click action to minimize (Requires dash-to-dock extension)
# gsettings set org.gnome.shell.extensions.dash-to-dock click-action 'minimize' # Uncomment if using dash-to-dock
# Open folder on drag-and-drop hover in Nautilus
gsettings set org.gnome.nautilus.preferences open-folder-on-dnd-hover true
# Allow volume above 100%
gsettings set org.gnome.desktop.sound allow-volume-above-100-percent true
# Enable fractional scaling (Wayland)
gsettings set org.gnome.mutter experimental-features "['scale-monitor-framebuffer']"
```

### Recommended GNOME Extensions
Install via <https://extensions.gnome.org/> after installing `gnome-shell-extensions` and the browser connector.
1.  [Advanced Alt+Tab Window Switcher](https://extensions.gnome.org/extension/4412/advanced-alttab-window-switcher/)
2.  [Alphabetical App Grid](https://extensions.gnome.org/extension/4269/alphabetical-app-grid/)
3.  [Caffeine](https://extensions.gnome.org/extension/517/caffeine/)
4.  [Color Picker](https://extensions.gnome.org/extension/3396/color-picker/)
5.  [Logo Menu](https://extensions.gnome.org/extension/4451/logo-menu/)
6.  [User Themes](https://extensions.gnome.org/extension/19/user-themes/)
7.  [Clipboard Indicator](https://extensions.gnome.org/extension/779/clipboard-indicator/)
8.  [Desktop Icons NG (DING)](https://extensions.gnome.org/extension/2087/desktop-icons-ng-ding/)
9.  [AppIndicator Support](https://extensions.gnome.org/extension/615/appindicator-support/)
10. [Vitals](https://extensions.gnome.org/extension/1460/vitals/)
11. [Just Perfection](https://extensions.gnome.org/extension/3843/just-perfection/)

### Fix Application Icons in Dash/Dock
The process is the same as described in the Ubuntu README. Find the `.desktop` file (usually in `/usr/share/applications/` or `~/.local/share/applications/`) and add/modify the `StartupWMClass` line.

### Add Wezterm to Nautilus Context Menu
Follow the instructions here: [nautilus-open-any-terminal](https://github.com/Stunkymonkey/nautilus-open-any-terminal) (Requires Python and `python-nautilus`).
```bash
sudo pacman -S python python-nautilus
```

## Development & Editors

### Neovim (LazyVim Starter)
Install Neovim:
```bash
sudo pacman -S neovim
```
If you have an existing Neovim config (`~/.config/nvim`), back it up first.
```bash
git clone https://github.com/LazyVim/starter ~/.config/nvim
rm -rf ~/.config/nvim/.git
```

### VS Code
Install from the AUR:
```bash
# Using an AUR helper:
yay -S visual-studio-code-bin
```

## Useful Applications

### Multimedia & Graphics
```bash
sudo pacman -S vlc gimp ffmpeg nomacs mpv obs-studio
```

### Disk Usage Analyzer
```bash
sudo pacman -S baobab
```

### PDF Arranger (Flatpak)
[Install from Flathub](https://flathub.org/apps/com.github.jeromerobert.pdfarranger)
```bash
flatpak install flathub com.github.jeromerobert.pdfarranger
```

### Upscayl Image Upscaler (Flatpak)
[Install from Flathub](https://flathub.org/apps/org.upscayl.Upscayl)
```bash
flatpak install flathub org.upscayl.Upscayl
```

### Drawpile Collaborative Drawing
Install from official repositories or AUR:
```bash
sudo pacman -S drawpile
# or using an AUR helper: yay -S drawpile
```

### ExcaliDraw Whiteboard
[Web Application Link](https://excalidraw.com/) or [GitHub Repo](https://github.com/excalidraw/excalidraw)

### Web Browsers (AUR)
Install using an AUR helper:
```bash
yay -S google-chrome
yay -S microsoft-edge-stable-bin
```

## Virtualization & Containers

### Distrobox
Install Distrobox (check official repos first, then AUR):
```bash
sudo pacman -S distrobox
# or using an AUR helper: yay -S distrobox
```
*Ensure `~/.local/bin` is in your PATH if installed manually.*

[Docker: Non Shared Mounts Compatibility Info](https://github.com/89luca89/distrobox/blob/main/docs/compatibility.md#non-shared-mounts)

### Podman (Alternative to Docker)
Install Podman:
```bash
sudo pacman -S podman
```
*(The `install_podman.sh` script in this repo provides a way to install a specific static version if needed, but the `pacman` version is usually preferred.)*

## Optional / Advanced

### Snap Packages
Install Snap daemon and enable the service:
```bash
sudo pacman -S snapd
sudo systemctl enable --now snapd.socket
# Optional: Create classic snap support link
sudo ln -s /var/lib/snapd/snap /snap
# Optional: For snap GUI apps needing theme integration
# yay -S snapd-glib
```
Refresh installed snaps:
```bash
sudo snap refresh
```
Install optional packages via Snap:
```bash
# Example: sudo snap install package-name
```
Install other optional packages (Arch equivalents):
```bash
# Codecs (equivalent to parts of ubuntu-restricted-extras)
sudo pacman -S gst-plugins-good gst-plugins-bad gst-plugins-ugly gst-libav

# Other tools
sudo pacman -S dconf-editor timeshift terminator qt6-base # qt5-base if needed for specific apps
```

### Powerlevel10k Zsh Theme
```bash
git clone --depth=1 https://github.com/romkatv/powerlevel10k.git ${ZSH_CUSTOM:-$HOME/.oh-my-zsh/custom}/themes/powerlevel10k
```
*Set `ZSH_THEME="powerlevel10k/powerlevel10k"` in your `~/.zshrc` and run `p10k configure`.*

### Bluetooth Service
Install Bluetooth packages and enable the service:
```bash
sudo pacman -S bluez bluez-utils
sudo systemctl enable bluetooth.service && sudo systemctl start bluetooth.service
```

### Sudo Path Configuration
If `sudo` commands can't find binaries installed in user paths (like Homebrew), you might need to configure `secure_path` in `/etc/sudoers`. Use `sudo visudo` to edit.
[See Arch Wiki: Sudo#Environment variables](https://wiki.archlinux.org/title/Sudo#Environment_variables)

### ZRam Setup
Arch Linux provides several ways to set up ZRam. Using `systemd-zram-generator` is common:
1. Install the package: `sudo pacman -S systemd-zram-generator`
2. Configure it via `/etc/systemd/zram-generator.conf`. A simple example:
   ```ini
   [zram0]
   zram-size = ram / 2
   ```
3. Reboot or manually start the generated service (`sudo systemctl start /dev/zram0`).

Alternatively, consult the [Arch Wiki: Improving performance#Zram or zswap](https://wiki.archlinux.org/title/Improving_performance#Zram_or_zswap) or use other AUR packages like `zramd`.

[General ZRam Info Link](https://fosspost.org/enable-zram-on-linux-better-system-performance/)

## Other Notes

*   Remember to consult the [Arch Wiki](https://wiki.archlinux.org/) for the most accurate and up-to-date information for Arch Linux. It is an invaluable resource.
