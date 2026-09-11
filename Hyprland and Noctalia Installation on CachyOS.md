# Hyprland and Noctalia on CachyOS

This guide documents the current CachyOS installation path for Hyprland with
Noctalia v5. It was checked against the CachyOS and Noctalia documentation on
2026-09-11.

## Recommended installation

CachyOS provides `cachyos-hypr-noctalia`, a settings/meta package that installs
Hyprland, Noctalia, UWSM, the Hyprland desktop portal, CachyOS configuration
files, and the supporting desktop applications.

Install the CachyOS Hyprland/Noctalia bundle with one command:

```bash
sudo pacman -Syu cachyos-hypr-noctalia
```

If you use `paru`, the equivalent command is:

```bash
paru -Syu cachyos-hypr-noctalia
```

The package manager resolves the required dependencies automatically. The
bundle directly includes:

- `hyprland`, `noctalia`, `uwsm`
- `xdg-desktop-portal-hyprland`, `grim`, `slurp`, `wl-clipboard`
- `brightnessctl`, `hyprpicker`, `satty`
- `kitty`, `dolphin`, `gnome-calculator`, `gnome-text-editor`
- `qt6ct`, `nwg-look`, `adw-gtk-theme`, fonts, and CachyOS defaults

If installing for an existing user, back up the current configuration and copy
the CachyOS defaults:

```bash
cp -a ~/.config ~/.config.backup-$(date +%F-%H%M%S)
cp -a /etc/skel/.config/. ~/.config/
```

For a clean setup, CachyOS recommends creating a separate user instead of
overwriting the configuration of another desktop environment:

```bash
sudo useradd -m -s /bin/zsh <new_user>
sudo passwd <new_user>
```

Reboot, then choose **Hyprland (UWSM)** in the display manager. The UWSM
session is preferred over launching plain Hyprland.

```bash
reboot
```

After logging in:

- Run `hyprctl monitors` and edit
  `~/.config/hypr/config/monitors.lua` for monitor-specific settings.
- Edit `~/.config/uwsm/env` for user-specific Wayland environment variables.
- Open Noctalia settings with **Super+Z**.

## Installing only the core packages

Use this when the CachyOS bundle is not wanted:

```bash
sudo pacman -Syu hyprland noctalia uwsm \
  xdg-desktop-portal xdg-desktop-portal-hyprland xdg-desktop-portal-gtk \
  matugen cliphist wl-clipboard grim slurp qt6ct qt5ct --needed
```

`noctalia` is the maintained Noctalia v5 package in the Arch/CachyOS
repositories. Do not use old `noctalia-shell` v4 instructions unless an
archived v4 installation is specifically required.

Noctalia's packaged runtime dependencies include Wayland, Cairo, Pango,
Fontconfig, FreeType, PipeWire/WirePlumber, Polkit, `libsecret`, `librsvg`,
`libqalculate`, `libwebp`, `libjxl`, `libxml2`, `sdbus-cpp`, `jemalloc`, and
related libraries. `pacman` installs these automatically. Building Noctalia
manually would additionally require development tools such as `meson`, `gcc`,
`just`, `ninja`, and the corresponding `-devel` libraries; that is unnecessary
when using the CachyOS package.

## Optional integrations

Install these only when the feature is needed:

```bash
# Battery and power-profile integration
sudo pacman -S --needed power-profiles-daemon upower
sudo systemctl enable --now power-profiles-daemon

# External-monitor brightness control
sudo pacman -S --needed ddcutil

# Media-key controls
sudo pacman -S --needed playerctl
```

`ddcutil` is optional and can be unstable with some monitors. Noctalia also
supports `noctalia-greeter` or `sddm` as optional display managers. A display
manager is not required if Hyprland is started from a TTY.

For SDDM on a system without another display manager:

```bash
sudo pacman -S --needed sddm
sudo systemctl enable --now sddm
```

## Verification

Check the main packages and the available sessions:

```bash
pacman -Q cachyos-hypr-noctalia hyprland noctalia uwsm \
  xdg-desktop-portal-hyprland
ls /usr/share/wayland-sessions/
```

The expected session files include `hyprland.desktop` and
`hyprland-uwsm.desktop`.

### Alt + Tab switcher + hyprmod

```bash
paru -S snappy-switcher hyprmod
```

### Some extra packages
```bash
sudo pacman -S nautilus qt6-declarative qt6-5compat qt6-svg qt6-multimedia qt6-multimedia-ffmpeg gst-plugins-base gst-plugins-good gst-plugins-bad gst-plugins-ugly --needed
```

### Gnome keyring
```bash
sudo pacman -S gnome-keyring
systemctl --user enable --now gnome-keyring-daemon.socket
```

## Sources

- [CachyOS Hyprland post-install guide](https://wiki.cachyos.org/configuration/desktop_environments/hyprland/)
- [Noctalia v5 installation guide](https://docs.noctalia.dev/noctalia/getting-started/installation/)
- [CachyOS Hyprland/Noctalia settings package](https://dashboard.cachyos.org/package/cachyos/any/cachyos-hypr-noctalia)
- [CachyOS Hyprland/Noctalia configuration repository](https://github.com/CachyOS/cachyos-hypr-noctalia)
