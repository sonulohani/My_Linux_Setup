# Build Ghostty on ubuntu 24.04

## Install build dependencies
```bash
sudo apt install meson ninja-build libwayland-dev wayland-protocols \
libgtk-4-dev gobject-introspection libgirepository1.0-dev valac \
libadwaita-1-dev gettext libxml2-utils
````

## Clone and build gtk4-layer-shell

```bash
git clone https://github.com/wmww/gtk4-layer-shell.git
cd gtk4-layer-shell
meson setup build
ninja -C build
sudo ninja -C build install
sudo ldconfig
```

## Rebuild Ghostty

```bash
cd ~/Downloads/ghostty
zig build -Doptimize=ReleaseFast
```

## Install Ghostty

Copy the `zig-out` directory contents to `/usr/local`.

## Update the icon database

```bash
sudo gtk-update-icon-cache -f -t /usr/local/share/icons/hicolor/
```

---

# Ghostty Configuration

Create the config file at:

```bash
~/.config/ghostty/config
```

Paste the following configuration:

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

# === NEW in 1.2: Quick Terminal (Dropdown) ===
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

---

# Setting Ghostty as Default Terminal (Nemo)

Run the following command to set Ghostty as the default for Nemo with the correct directory flag:

```bash
gsettings set org.cinnamon.desktop.default-applications.terminal exec 'ghostty'
```

Then, specifically for Nemo’s behavior, run:

```bash
gsettings set org.cinnamon.desktop.default-applications.terminal exec 'ghostty --working-directory=%P'
```

