# Niri Window Manager & Noctalia Shell

Setup guide for [Niri](https://github.com/niri-wm/niri) (scrollable-tiling Wayland compositor) with [Noctalia Shell](https://github.com/noctalia-dev/noctalia) on CachyOS / Arch Linux.

---

## Quick Install (CachyOS)

CachyOS ships a meta package that pulls in Niri, Noctalia, and the default configuration skeleton:

```bash
sudo pacman -S cachyos-niri-noctalia
```

After installation, copy the default config into your home directory:

```bash
cp -r /etc/skel/.config/* "$HOME/.config/"
```

Log out and select the **Niri** session from your display manager, or start it from a TTY.

---

## Manual Install (AUR / paru)

If you prefer to install packages individually or are on stock Arch:

```bash
paru -S niri xwayland-satellite alacritty fuzzel imagemagick brightnessctl git python \
  mako waybar noctalia-shell niri-settings-git xdg-desktop-portal-gnome swaybg \
  swayidle swaylock udiskie wlsunset cliphist wl-clipboard wtype
```

Then copy the default configuration:

```bash
cp -r /etc/skel/.config/* "$HOME/.config/"
```

### Package overview

| Package | Purpose |
| --- | --- |
| `niri` | Wayland compositor |
| `noctalia-shell` | Desktop shell (bar, widgets, settings) |
| `niri-settings-git` | GUI for editing Niri config |
| `xwayland-satellite` | XWayland support for legacy X11 apps |
| `alacritty` | Terminal emulator |
| `fuzzel` | Application launcher |
| `waybar` | Status bar (if not using Noctalia bar exclusively) |
| `mako` | Notification daemon |
| `swaybg` / `swayidle` / `swaylock` | Wallpaper, idle, and lock screen |
| `udiskie` | Automount removable drives |
| `wlsunset` | Blue-light filter |
| `cliphist` / `wl-clipboard` | Clipboard history backend |
| `wtype` | Wayland text injection (used by Clipper auto-paste) |
| `xdg-desktop-portal-gnome` | Desktop portal for file dialogs, screen share, etc. |

---

## Clipboard History (cliphist)

Niri and Noctalia do not manage clipboard history on their own. Use `cliphist` with `wl-paste` watchers started at login.

Add the following to `$HOME/.config/niri/cfg/autostart.kdl`:

```kdl
    // Listen for text copies
    spawn-sh-at-startup "wl-paste --type text --watch cliphist store"

    // Listen for image/binary copies
    spawn-sh-at-startup "wl-paste --type image --watch cliphist store"
```

Reload Niri or restart the session for the watchers to take effect.

To verify cliphist is receiving entries:

```bash
cliphist list
```

---

## Noctalia Clipper Plugin

The [Clipper](https://noctalia.dev/plugins/clipper) plugin provides a searchable clipboard history panel, pinned items, NoteCards, and optional auto-paste. It uses `cliphist` as its backend (installed above).

### Install from Noctalia Settings

1. Open **Noctalia Settings** (from the shell bar or run `noctalia-settings`).
2. Go to **Plugins**.
3. Search for **Clipper**.
4. Click **Install**.
5. **Reload Noctalia Shell** when prompted.

Plugin data is stored under `~/.config/noctalia/plugins/clipper/`.

### Optional: toggle keybind in Niri

Bind `Super+V` to open the Clipper panel. Add to your Niri binds config (e.g. `~/.config/niri/config.kdl` or the relevant binds include):

```kdl
  // ---- Clipboard History ----
    Mod+V                               { spawn-sh "qs -c noctalia-shell ipc call plugin:clipper toggle"; }
```

You can also run the toggle from a terminal:

```bash
qs -c noctalia-shell ipc call plugin:clipper toggle
```

### Clipper settings worth enabling

In **Noctalia Settings → Plugins → Clipper**:

- **Auto-Paste** — pastes the selected item into the focused window (requires `wtype`).
- **NoteCards** — sticky notes panel for quick capture.
- **Appearance** — per-card-type color customization with live preview.

### Troubleshooting clipboard history

If the Clipper panel is empty but copies work elsewhere:

```bash
# Restart clipboard watchers
pkill wl-paste
# Re-login, or re-add the spawn-sh-at-startup lines and reload niri
```

Ensure `cliphist` and `wl-clipboard` are installed and the autostart watchers above are active.

---

## Flameshot (screenshots)

[Flameshot](https://flameshot.org/) is a screenshot tool with annotation support. On Wayland, capture the selection to the clipboard with a Niri keybind.

Install via Flatpak:

```bash
flatpak install flathub org.flameshot.Flameshot
```

Add to your Niri binds config (e.g. `~/.config/niri/config.kdl` or the relevant binds include):

```kdl
  // ---- Flameshot (screenshot tool) ----
    Mod+CTRL+ALT+Shift+P                { spawn-sh "flatpak run org.flameshot.Flameshot gui --raw | wl-copy"; }
```

`--raw` pipes the image bytes to `wl-copy` so the screenshot lands on the clipboard (works with the cliphist watchers above).

---

## Power Profiles (Battery & Power Management)

Noctalia is built as a pure desktop shell and intentionally avoids embedding system-level hardware management (like CPU governors or laptop power-saving states) directly into its core engine.

Instead, managing system power profiles inside a Niri + Noctalia setup is accomplished using a Noctalia plugin integrated with a standard system daemon backend like Linux's `power-profiles-daemon` or `tlp`.

### The Recommended Approach: Battery & Power Management Plugin

Noctalia features a dedicated, theme-integrated plugin that embeds a dynamic battery indicator into your status bar and provides an interactive popup panel to toggle between **Performance**, **Balanced**, and **Power Saver** modes.

#### Step 1: Install the system backend

Before installing the UI widget, make sure your Linux system has an active daemon running that can actually change your CPU/GPU hardware profiles. For most modern hardware and laptops, `power-profiles-daemon` is the clean, conflict-free standard.

```bash
# For Arch Linux
sudo pacman -S power-profiles-daemon
sudo systemctl enable --now power-profiles-daemon

# For Fedora (usually installed by default, but to ensure it is active)
sudo systemctl enable --now power-profiles-daemon
```

Verify it's working by running `powerprofilesctl` in your terminal to see your hardware's available modes.

#### Step 2: Install the Noctalia plugin

1. Open **Noctalia Settings** (from the shell bar, run `noctalia-settings`, or use your mapped UI keybinding).
2. Go to **Plugins**.
3. Search for **Battery & Power Management Plugin**.
4. Click **Install**, then toggle it **Enabled**.

Once activated, it embeds into your existing top or bottom status bar. Click the battery icon to open an overlay panel that shows live power draw in watts and buttons to switch power profiles instantly.

### Optional: keyboard-driven profile switching

To shift power profiles via keyboard shortcuts without opening a GUI panel, bind `powerprofilesctl` directly in your Niri configuration. Add to your binds config (e.g. `~/.config/niri/config.kdl` or the relevant binds include):

```kdl
  // ---- Power profiles ----
    Mod+F1                              { spawn-sh "powerprofilesctl set power-saver"; }
    Mod+F2                              { spawn-sh "powerprofilesctl set balanced"; }
    Mod+F3                              { spawn-sh "powerprofilesctl set performance"; }
```

Niri hot-reloads its configuration on save, so `Super+F1/F2/F3` take effect immediately.

---

## Resources

- [Niri documentation](https://niri-wm.github.io/niri/)
- [Niri — ArchWiki](https://wiki.archlinux.org/title/Niri)
- [Noctalia Shell](https://github.com/noctalia-dev/noctalia)
- [Clipper plugin docs](https://noctalia.dev/plugins/clipper)
- [Flameshot](https://flameshot.org/)
- [power-profiles-daemon — ArchWiki](https://wiki.archlinux.org/title/CPU_frequency_scaling#power-profiles-daemon)
