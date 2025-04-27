# Ubuntu 24.04+ Setup Guide

This guide provides instructions for setting up an Ubuntu 24.04+ system with essential tools and configurations.

## System Updates

Keep your system up-to-date:
```bash
sudo apt update && sudo apt upgrade
```

## Essential Packages & Setup

### Core Development & System Tools
```bash
sudo apt install -y python3-pip build-essential binutils cmake-qt-gui \
g++ gdb git rar unrar p7zip-full p7zip-rar fonts-dejavu \
htop xclip meld curl wget extra-cmake-modules \
mesa-common-dev libglu1-mesa-dev gettext ninja-build \
libtool libtool-bin autoconf automake pkg-config unzip fonts-hack-ttf \
zsh python3-virtualenv preload mc \
lazygit fastfetch ripgrep fd-find aria2 bat neovim ranger trash-cli hwatch
```
*Note: The `bat` package installs as `batcat` on Ubuntu. You might want to create a symlink: `ln -s $(which batcat) ~/.local/bin/bat`.*
*Note: The `fd-find` package installs as `fdfind`. You might want to create a symlink: `ln -s $(which fdfind) ~/.local/bin/fd`.*
*Ensure `~/.local/bin` is in your PATH for the symlinks to work.*

### Enable Firewall (ufw)
```bash
sudo ufw enable
```

### Enable SSD Trim (fstrim.timer)
```bash
sudo systemctl enable fstrim.timer && sudo systemctl start fstrim.timer
```

### Flatpak Setup
Configure Flathub repository:
```bash
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
Install Wezterm:
```bash
# Add repository key
curl -fsSL https://apt.fury.io/wez/gpg.key | sudo gpg --yes --dearmor -o /usr/share/keyrings/wezterm-fury.gpg
# Add repository source
echo 'deb [signed-by=/usr/share/keyrings/wezterm-fury.gpg] https://apt.fury.io/wez/ * *' | sudo tee /etc/apt/sources.list.d/wezterm.list
# Install
sudo apt update && sudo apt install wezterm
```
[Wezterm Installation Docs](https://wezfurlong.org/wezterm/install/linux.html#installing-on-ubuntu-and-debian-based-systems)

### Oh My Zsh & Plugins
Install Oh My Zsh:
```bash
sh -c "$(curl -fsSL https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)"
```
Install Zsh plugins:
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
Enable plugins in `~/.zshrc`:
```bash
sed -i 's/^plugins=(git)/plugins=(git zsh-autosuggestions zsh-syntax-highlighting you-should-use zsh-safe-rm emoji emotty)/' ~/.zshrc
```
*Remember to source your `~/.zshrc` or restart your shell after modifying it.*

### Atuin Shell History
Install Atuin for enhanced shell history:
```bash
curl --proto '=https' --tlsv1.2 -LsSf https://setup.atuin.sh | sh
```

### Zellij Terminal Multiplexer
[Zellij Website](https://zellij.dev/) (Installation instructions available on the website)

### Kitty Terminal
Install Kitty terminal emulator:
```bash
# Install Kitty via official script
curl -L https://sw.kovidgoyal.net/kitty/installer.sh | sh /dev/stdin

# Create symbolic links to add kitty and kitten to PATH
# (assuming ~/.local/bin is in your system-wide PATH)
ln -sf ~/.local/kitty.app/bin/kitty ~/.local/kitty.app/bin/kitten ~/.local/bin/

# Place the kitty.desktop file for application menu integration
cp ~/.local/kitty.app/share/applications/kitty.desktop ~/.local/share/applications/

# Update the paths in the desktop file
sed -i "s|Icon=kitty|Icon=$(readlink -f ~)/.local/kitty.app/share/icons/hicolor/256x256/apps/kitty.png|g" ~/.local/share/applications/kitty.desktop
sed -i "s|Exec=kitty|Exec=$(readlink -f ~)/.local/kitty.app/bin/kitty|g" ~/.local/share/applications/kitty.desktop

# Optional: If you want kitty to be the default for xdg-terminal-exec
# echo 'kitty.desktop' > ~/.config/xdg-terminals.list
```
[Kitty Terminfo Fix](https://sw.kovidgoyal.net/kitty/faq/#i-get-errors-about-the-terminal-being-unknown-or-opening-the-terminal-failing-or-functional-keys-like-arrow-keys-don-t-work)

## Desktop Environment (GNOME)

### Essential GNOME Packages & Tweaks
```bash
# Install Tweaks tool and Extension support
sudo apt install gnome-tweaks gnome-shell-extensions

# Center new windows
gsettings set org.gnome.mutter center-new-windows true
# Set dash-to-dock click action to minimize
gsettings set org.gnome.shell.extensions.dash-to-dock click-action 'minimize'
# Open folder on drag-and-drop hover in Nautilus
gsettings set org.gnome.nautilus.preferences open-folder-on-dnd-hover true
# Allow volume above 100%
gsettings set org.gnome.desktop.sound allow-volume-above-100-percent true
# Enable fractional scaling (Wayland)
gsettings set org.gnome.mutter experimental-features "['scale-monitor-framebuffer']"

```

### Recommended GNOME Extensions
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
If an application icon isn't displaying correctly:
1.  Launch the application (e.g., Terminator).
2.  Run `xprop WM_CLASS` in a terminal. Click the application window. Note the `WM_CLASS` string (e.g., `"Terminator", "Terminator"`).
3.  Find the application's `.desktop` file (usually in `/usr/share/applications/` or `~/.local/share/applications/`).
4.  Edit the file (e.g., `sudo nano /usr/share/applications/terminator.desktop`) and add/modify the `StartupWMClass` line using the *second* value from step 2 (without quotes):
    ```ini
    StartupWMClass=Terminator
    ```
5.  Save the file. You might need to log out and back in.

### Add Wezterm to Nautilus Context Menu
Follow the instructions here: [nautilus-open-any-terminal](https://github.com/Stunkymonkey/nautilus-open-any-terminal)

## Development & Editors

### Neovim (LazyVim Starter)
If you have an existing Neovim config (`~/.config/nvim`), back it up first.
```bash
git clone https://github.com/LazyVim/starter ~/.config/nvim
rm -rf ~/.config/nvim/.git
```

### VS Code
[Download .deb from VS Code Website](https://code.visualstudio.com/)
```bash
# After downloading:
sudo apt install ./<downloaded_vscode_file>.deb
```

## Useful Applications

### Multimedia & Graphics
```bash
sudo apt install -y vlc gimp ffmpeg nomacs mpv obs-studio
```

### Disk Usage Analyzer
```bash
sudo apt install baobab
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
[Download from GitHub Releases](https://github.com/drawpile/drawpile/releases) (AppImage recommended for easy use)

### ExcaliDraw Whiteboard
[Web Application Link](https://excalidraw.com/) or [GitHub Repo](https://github.com/excalidraw/excalidraw)

### Web Browsers (.deb)
1.  [Google Chrome](https://www.google.com/intl/en_in/chrome/)
2.  [Microsoft Edge](https://www.microsoft.com/en-gb/edge)

## Virtualization & Containers

### Distrobox
Install Distrobox for managing containerized environments:
```bash
curl -s https://raw.githubusercontent.com/89luca89/distrobox/main/install | sh -s -- --next --prefix ~/.local
```
*Ensure `~/.local/bin` is in your PATH.*

[Docker: Non Shared Mounts Compatibility Info](https://github.com/89luca89/distrobox/blob/main/docs/compatibility.md#non-shared-mounts)

### Podman (Alternative to Docker)
See `install_podman.sh` script in this repository.

## Optional / Advanced

### Snap Packages
Refresh installed snaps:
```bash
sudo snap refresh
```
Install optional packages via Snap:
```bash
# Example: sudo snap install package-name
```
Install other optional apt packages:
```bash
sudo apt install -y ubuntu-restricted-extras dconf-editor timeshift terminator snapd qt5-default
```

### Powerlevel10k Zsh Theme
```bash
git clone --depth=1 https://github.com/romkatv/powerlevel10k.git ${ZSH_CUSTOM:-$HOME/.oh-my-zsh/custom}/themes/powerlevel10k
```
*Set `ZSH_THEME="powerlevel10k/powerlevel10k"` in your `~/.zshrc` and run `p10k configure`.*

### Bluetooth Service
Ensure Bluetooth service is running:
```bash
sudo systemctl enable bluetooth.service && sudo systemctl start bluetooth.service
```

### Sudo Path Configuration
If `sudo` commands can't find binaries installed in user paths (like Homebrew):
[See Super User Answer](https://superuser.com/a/927599)

### ZRam Setup
For improved performance on systems with limited RAM:
[ZRam Setup Guide](https://fosspost.org/enable-zram-on-linux-better-system-performance/)

<!-- To remove apt key deprecated warning due to above commands follow the instruction here:
https://askubuntu.com/questions/1398344/apt-key-deprecation-warning-when-updating-system -->
