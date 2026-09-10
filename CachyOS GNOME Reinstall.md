## Fresh CachyOS installation

1. Install the **GNOME** edition and choose the proprietary/open NVIDIA option
   appropriate for this same laptop.
2. Update before adding applications:

```bash
sudo pacman -Syu
```

3. Make sure Flathub is configured:

```bash
sudo pacman -S --needed flatpak
flatpak remote-add --if-not-exists flathub \
  https://dl.flathub.org/repo/flathub.flatpakrepo
```

## Main packages

`paru` can install packages from the CachyOS/Arch repositories and the AUR. The
following groups reflect the useful non-default software on the current system.

### Desktop tools

```bash
paru -S --needed \
  extension-manager gnome-tweaks gnome-shell-extensions \
  gnome-browser-connector dconf-editor gdm-settings \
  flameshot pavucontrol meld gnome-rounded-blur pipewire-control-center \
  ptyxis nautilus-open-any-terminal
```


```bash
gsettings set com.github.stunkymonkey.nautilus-open-any-terminal terminal kitty
gsettings set com.github.stunkymonkey.nautilus-open-any-terminal keybindings '<Ctrl><Alt>t'
gsettings set com.github.stunkymonkey.nautilus-open-any-terminal new-tab true
gsettings set com.github.stunkymonkey.nautilus-open-any-terminal flatpak system
```

### Browsers and productivity

```bash
paru -S --needed \
  brave-bin vivaldi microsoft-edge-stable-bin \
  joplin-desktop onlyoffice-bin
```

### Media and creative applications

```bash
paru -S --needed \
  gimp obs-studio vlc vlc-plugins-all
```

### Development and containers

```bash
paru -S --needed \
  base-devel git git-lfs neovim visual-studio-code-bin \
  cmake ninja lldb nodejs npm ripgrep fd gdb \
  docker docker-buildx docker-compose distrobox clang
```

### Terminal and system utilities

```bash
paru -S --needed \
  kitty alacritty micro btop htop glances duf fastfetch \
  aria2 7zip unrar unzip wl-clipboard \
  keyd profile-sync-daemon ufw
```

`keyd.service` is enabled now, but no mapping files were found under `/etc/keyd`.
Skip `keyd` unless a mapping is added before the reinstall.

### Fonts, icons, and cursors

```bash
paru -S --needed \
  inter-font ttf-fira-code ttf-jetbrains-mono ttf-meslo-nerd \
  awesome-terminal-fonts bibata-cursor-theme \
  catppuccin-cursors-mocha gtk-engine-murrine
```

The current desktop also uses assets that are installed only in the home
directory and must be restored from the archive:

- UI font: **Inter 10** (package above)
- Monospace font: **Maple Mono NF 10** from `~/.local/share/fonts`
- Icon theme: **Tela Nord Light** from `~/.local/share/icons/Tela-nord-light`
- Cursor theme: **Catppuccin Mocha Lavender** (package above)
- Colloid Catppuccin themes from `~/.themes`
- GNOME Shell user-theme setting: `default-pure`; its matching theme directory
  was not found during this inventory, so GNOME may currently be falling back

Refresh font and icon caches after restoring local assets:

```bash
fc-cache -fv
gtk-update-icon-cache -f -t "$HOME/.local/share/icons/Tela-nord-light"
```

## Flatpak applications

```bash
flatpak install -y flathub \
  com.github.tchx84.Flatseal \
  com.valvesoftware.Steam \
  net.meshlab.MeshLab
```

There are currently no Snap packages installed.

## GNOME extensions

Install extensions through **Extension Manager** after the first update and
reboot. Search by the display name and verify the UUID where shown.

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
12. [Others](https://itsfoss.com/gnome-extensions-customization/)
13. [Wack Sonoma Lockscreen](https://github.com/rinzler69-wastaken/wack-sonoma-lockscreen)
14: [Auto Accent Colour](https://extensions.gnome.org/extension/7502/auto-accent-colour)
15. [Blur My Shell](https://github.com/aunetx/blur-my-shell)
16. [Compwiz windows effect](https://github.com/hermes83/compiz-windows-effect)
17. [Modern Clock](https://github.com/Tony-Rain/Modern-Clock-Gnome)

`User Themes` and `Removable Drive Menu` are supplied by the
`gnome-shell-extensions` package. Live Lock Screen currently points to
`~/Documents/softwares/qylock-main/themes/enfield/bg.mp4`, so restore that file
before enabling it.

## Services and groups

Enable the user-added services:

```bash
sudo systemctl enable --now docker.service ufw.service
systemctl --user enable --now psd.service
sudo usermod -aG docker "$USER"
```

Log out once after adding the Docker group. If a real keyd configuration was
backed up, restore it and then run:

```bash
sudo systemctl enable --now keyd.service
```

The CachyOS installation currently enables its own performance, laptop, GPU,
network, and snapshot services, including `ananicy-cpp`, `bpftune`, `cpupower`,
`intel_lpmd`, `nvidia-powerd`, `thermald`, NetworkManager, Bluetooth, Snapper
timers, and `fstrim.timer`. Prefer CachyOS package presets for these instead of
manually enabling them all on a new installation.
