# Build Ghostty in ubuntu 24.04

## Install build dependencies
```bash
sudo apt install meson ninja-build libwayland-dev wayland-protocols \
libgtk-4-dev gobject-introspection libgirepository1.0-dev valac
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
