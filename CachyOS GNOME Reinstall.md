# CachyOS GNOME Reinstall Checklist

Inventory captured on **2026-08-22** from CachyOS running **GNOME 50.4 on
Wayland**. The current machine has Intel Meteor Lake graphics plus an NVIDIA RTX
2000 Ada laptop GPU.

This is a curated restore list. CachyOS marks many installer-provided packages
as explicitly installed, so reinstalling the complete `pacman -Qqe` output would
also pull in a large amount of default and hardware support software.

## Before formatting

Save exact package and extension inventories:

```bash
backup_dir="$HOME/cachyos-reinstall-backup-$(date +%F)"
mkdir -p "$backup_dir"

pacman -Qqen > "$backup_dir/pacman-official.txt"
pacman -Qqem > "$backup_dir/pacman-foreign.txt"
flatpak list --app --columns=application > "$backup_dir/flatpak-apps.txt"
gnome-extensions list > "$backup_dir/gnome-extensions.txt"
gnome-extensions list --enabled > "$backup_dir/gnome-extensions-enabled.txt"
code --list-extensions > "$backup_dir/vscode-extensions.txt"
dconf dump / > "$backup_dir/gnome-dconf.ini"
```

Archive the small local configuration and desktop assets:

```bash
tar -C "$HOME" -czf "$backup_dir/user-configs.tar.gz" \
  .config/kitty \
  .config/alacritty \
  .config/Code/User \
  .local/share/applications \
  .local/share/gnome-shell/extensions \
  .local/share/fonts \
  .local/share/icons/Tela-nord-light \
  .themes
```

Copy the backup directory to another disk or cloud storage. Also back up these
larger paths separately if they are still needed:

- `~/Documents/softwares/qylock-main` (about 620 MB; Live Lock Screen asset)
- `~/Pictures/multi_monitor` (about 628 MB; wallpaper collection)
- `~/.local/bin/Cursor.AppImage` (about 286 MB)
- `~/Documents/softwares/Mako_Integrated_Simulator-x86_64.tar 2` (about 491 MB)
- `~/QtCreator` (about 3.0 GB; custom Qt Creator 7, 11, and 17 installs)
- `~/Qt` (about 5.8 GB; Qt SDK and Maintenance Tool)
- `~/.local/p4v` (about 516 MB; Perforce Visual Client)
- Any browser profiles not already synchronized
- SSH/GPG keys, Git configuration, projects, documents, and application data

The setup files already tracked in this repository include Kitty, Neovim,
Starship, Niri, and related configuration. Push the latest repository changes
before formatting.

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
  flameshot pavucontrol meld
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
  gimp obs-studio shotcut vlc vlc-plugins-all
```

### Development and containers

```bash
paru -S --needed \
  base-devel git git-lfs neovim visual-studio-code-bin \
  cmake ninja lldb nodejs npm ripgrep \
  docker docker-buildx docker-compose distrobox \
  p4 gp-saml-gui-git
```

`p4` and `gp-saml-gui-git` are currently foreign/AUR packages. The third
foreign package, `gtk-engine-murrine`, is included with the appearance packages
below.

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

## Graphics packages for this laptop

The current machine uses Intel integrated graphics and the NVIDIA open kernel
module. The CachyOS installer should select these automatically. Verify with:

```bash
pacman -Q \
  intel-ucode intel-media-driver vulkan-intel vpl-gpu-rt \
  linux-cachyos-nvidia-open nvidia-utils nvidia-prime nvidia-settings \
  libva-nvidia-driver lib32-nvidia-utils lib32-vulkan-intel
```

Install any missing packages only if reinstalling on the same hardware:

```bash
sudo pacman -S --needed \
  intel-ucode intel-media-driver vulkan-intel vpl-gpu-rt \
  linux-cachyos-nvidia-open nvidia-utils nvidia-prime nvidia-settings \
  libva-nvidia-driver lib32-nvidia-utils lib32-vulkan-intel
```

The system also has the LTS kernel and matching NVIDIA module as a fallback:

```bash
sudo pacman -S --needed \
  linux-cachyos-lts linux-cachyos-lts-headers linux-cachyos-lts-nvidia-open
```

## Flatpak applications

```bash
flatpak install -y flathub \
  com.github.tchx84.Flatseal \
  com.valvesoftware.Steam \
  net.meshlab.MeshLab
```

There are currently no Snap packages installed.

## Manually installed applications

These applications appear in the GNOME app grid but are not owned by Pacman or
Flatpak. Restore or reinstall their payloads, then restore
`~/.local/share/applications` from the configuration archive.

| Application | Current payload or launcher target |
| --- | --- |
| Cursor | `~/.local/bin/Cursor.AppImage` |
| Mako Integrated Simulator | `~/Documents/softwares/Mako_Integrated_Simulator-x86_64.tar 2` |
| Qt Creator 7.0.5, 11.0.8, and 17.0.1 | `~/QtCreator` |
| Qt Maintenance Tool and SDK | `~/Qt` |
| Perforce Visual Client (P4V) | `~/.local/p4v` |

Qt Creator 17 and P4V currently launch inside a Distrobox named
`ubuntu-22.04`. Its image is:

```text
artifactory.osep.stryker.com/osep-docker/strykercorp/osep/osep-build-tools/osep-cpp-build-tools:gcc-11
```

Recreate it after connecting to the required company network/registry:

```bash
distrobox create \
  --name ubuntu-22.04 \
  --image artifactory.osep.stryker.com/osep-docker/strykercorp/osep/osep-build-tools/osep-cpp-build-tools:gcc-11
```

The Distrobox container itself and any changes made inside it are not preserved
by copying the launchers. Record or export any container-only work separately
before formatting.

## GNOME extensions

Install extensions through **Extension Manager** after the first update and
reboot. Search by the display name and verify the UUID where shown.

### Enabled now

| Extension | UUID | Version |
| --- | --- | ---: |
| Alphabetical App Grid | `AlphabeticalAppGrid@stuarthayhurst` | 44 |
| AppIndicator and KStatusNotifierItem Support | `appindicatorsupport@rgcjonas.gmail.com` | 64 |
| Blur My Shell | `blur-my-shell@aunetx` | 72 |
| Caffeine | `caffeine@patapon.info` | 60 |
| Clipboard Indicator | `clipboard-indicator@tudmotu.com` | 71 |
| Dhruva | `dhruva@narkagni` | 10 |
| Just Perfection | `just-perfection-desktop@just-perfection` | 36 |
| Live Lock Screen | `live-lockscreen@nick-redwill` | 8 |
| User Themes | `user-theme@gnome-shell-extensions.gcampax.github.com` | 76 |
| Removable Drive Menu | `drive-menu@gnome-shell-extensions.gcampax.github.com` | system |

`User Themes` and `Removable Drive Menu` are supplied by the
`gnome-shell-extensions` package. Live Lock Screen currently points to
`~/Documents/softwares/qylock-main/themes/enfield/bg.mp4`, so restore that file
before enabling it.

### Installed but disabled

| Extension | UUID | Version |
| --- | --- | ---: |
| Dash to Dock | `dash-to-dock@micxgx.gmail.com` | 105 |
| Peek Bar | `peek-bar@rachalaraj.github.com` | 22 |

GNOME's settings database also contains stale enabled entries for GNOME
Clipboard, Wall Shuffle, and Fullscreen Avoider, but their extension files are
not currently installed. They are intentionally omitted from the restore list.

### Restore extension settings

Install the extensions first, then restore the GNOME settings backup:

```bash
dconf load / < "$HOME/cachyos-reinstall-backup-YYYY-MM-DD/gnome-dconf.ini"
```

Log out and back in after restoring. Check the enabled set with:

```bash
gnome-extensions list --enabled
```

Important current appearance settings are light mode, blue accent, 125% text
scaling, Inter 10, Maple Mono NF 10, Tela Nord Light icons, and Catppuccin Mocha
Lavender cursors.

## VS Code extensions

```bash
for extension in \
  moshfeu.compare-folders \
  ms-python.debugpy \
  ms-python.python \
  ms-python.vscode-pylance \
  ms-python.vscode-python-envs \
  ms-vscode.cmake-tools \
  ms-vscode.cpp-devtools \
  ms-vscode.cpptools
do
  code --install-extension "$extension"
done
```

VS Code Settings Sync can restore these automatically if it was enabled before
formatting.

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

## Final checks

```bash
# Confirm the desktop and graphics session
echo "$XDG_CURRENT_DESKTOP / $XDG_SESSION_TYPE"
lspci -k | grep -A3 -E 'VGA|3D'

# Confirm containers and firewall
docker run --rm hello-world
sudo ufw status

# Show missing packages from the saved exact inventories
comm -23 \
  <(sort "$HOME/cachyos-reinstall-backup-YYYY-MM-DD/pacman-official.txt") \
  <(pacman -Qq | sort)

# Confirm Flatpaks and extensions
flatpak list --app
gnome-extensions list --enabled
```

Review the `comm` output rather than installing it blindly; it will include
packages that were part of the old CachyOS installer profile.