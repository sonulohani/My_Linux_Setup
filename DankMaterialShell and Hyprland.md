# DankMaterialShell Git with Hyprland

Ensure the compositor, session, greeter, portals, and useful integrations are
installed:

```bash
paru -S --needed \
  hyprland uwsm sddm nwg-look qt6ct qt5ct \
  xdg-desktop-portal-hyprland xdg-desktop-portal-gtk \
  quickshell accountsservice dgop \
  matugen cava dankcalendar-bin \
  qt6-multimedia qt6-multimedia-ffmpeg \
  i2c-tools brightnessctl playerctl \
  cliphist wl-clipboard grim slurp xdg-terminal-exec \
  dms-shell-hyprland
```

Only Quickshell is strictly required by upstream DMS. The other DMS packages
enable their corresponding widgets and integrations.

### Build and install DSearch from Git

DSearch is installed directly from its Git repository in this setup, not with
`paru`. Its upstream README requires Go 1.24 or newer.

Install the build dependencies:

```bash
sudo pacman -S --needed base-devel git go
```

Clone, build, and install DSearch using the upstream commands:

```bash
mkdir -p "$HOME/Documents/github"
git clone https://github.com/AvengeMedia/danksearch.git \
  "$HOME/Documents/github/danksearch"
cd "$HOME/Documents/github/danksearch"
make && sudo make install && make install-service
```

The build installs the binary to `/usr/local/bin/dsearch` and the user unit to
`~/.config/systemd/user/dsearch.service`. Enable and start the search service:

```bash
systemctl --user enable --now dsearch.service
```

Check the source build and service:

```bash
dsearch version
systemctl --user status dsearch.service
```

Enable SDDM as the system display manager:

```bash
sudo systemctl enable sddm.service
```

Do not restart SDDM from inside a graphical session because doing so terminates
the session. Log out or reboot after finishing the setup.

## Generate the Hyprland configuration

Refer this for the service: https://danklinux.com/docs/dankmaterialshell/cli-doctor#services

Back up an existing Hyprland configuration before asking DMS to generate its
starter files:

```bash
backup_dir="$HOME/.config/hypr.backup-$(date +%F-%H%M%S)"
cp -a "$HOME/.config/hypr" "$backup_dir"
dms setup
```

On this machine, DMS generated a Hyprland 0.55+ Lua configuration under
`~/.config/hypr`. Its startup handler exports the environment and starts the
Hyprland session target:

```lua
hl.on("hyprland.start", function()
        hl.exec_cmd("dbus-update-activation-environment --systemd --all")
        hl.exec_cmd("systemctl --user start hyprland-session.target")
end)
```

The corresponding target is `~/.config/systemd/user/hyprland-session.target`.
The generated `~/.config/hypr/dms/` directory contains DMS colors, outputs,
layout, cursor, window rules, and keybinds.

## Bind DMS to the Hyprland session

Upstream recommends attaching DMS to the compositor session instead of enabling
it for every desktop. This prevents DMS from starting in GNOME or another
graphical session.

```bash
systemctl --user disable dms.service
systemctl --user add-wants hyprland-session.target dms.service
systemctl --user daemon-reload
```

Start it immediately when already inside Hyprland:

```bash
systemctl --user start hyprland-session.target
systemctl --user start dms.service
```

Do not also add `dms run` or `exec-once=dms run` to the Hyprland configuration;
that would launch a second shell instance.

Useful service checks:

```bash
systemctl --user status dms.service
systemctl --user list-dependencies hyprland-session.target --plain
journalctl --user -u dms.service -b
```

At the SDDM login screen, select **Hyprland (uwsm-managed)**. SDDM normally
remembers that choice for the next login.

## Install the Qylock SDDM theme

Qylock is not packaged in the official repositories or AUR, so install it from
its Git repository:

```bash
mkdir -p "$HOME/Documents/github"
git clone https://github.com/Darkkal44/qylock.git \
  "$HOME/Documents/github/qylock"
cd "$HOME/Documents/github/qylock"
```

For the existing checkout, update instead:

```bash
git -C "$HOME/Documents/github/qylock" pull --ff-only
cd "$HOME/Documents/github/qylock"
```

Install the complete Qt 6 theme dependency set:

```bash
sudo pacman -S --needed \
  sddm qt6-declarative qt6-5compat qt6-svg \
  qt6-multimedia qt6-multimedia-ffmpeg \
  gst-plugins-base gst-plugins-good gst-plugins-bad gst-plugins-ugly \
  fzf
```

Run Qylock's interactive SDDM installer:

```bash
chmod +x sddm.sh
./sddm.sh
```

Choose the modern **Qt6** backend and then the desired theme. The script copies
the selected theme to `/usr/share/sddm/themes/` and updates
`/etc/sddm.conf.d/theme.conf`. The current machine uses `last-of-us`; `enfield`
is another available video theme.

Preview the selected theme without logging out:

```bash
sddm-greeter-qt6 --test-mode --theme /usr/share/sddm/themes/last-of-us
```

If the virtual keyboard opens at the greeter, create
`/etc/sddm.conf.d/virtualkeyboard.conf` with:

```ini
[General]
InputMethod=
```

## Optional: use Qylock after login

This is optional. Keep the DMS lock if only the SDDM greeter needs Qylock's
appearance.

To use a matching Qylock theme as the Hyprland session lock:

```bash
cd "$HOME/Documents/github/qylock"
chmod +x quickshell.sh
./quickshell.sh
```

The installer deploys the lockscreen to
`~/.local/share/quickshell-lockscreen/lock.sh` and saves the selected theme in
`~/.config/qylock/theme`. Test it from Hyprland before changing a keybind:

```bash
"$HOME/.local/share/quickshell-lockscreen/lock.sh"
```

After confirming authentication works, change the existing lock keybind command
from:

```text
dms ipc call lock lock
```

to:

```text
~/.local/share/quickshell-lockscreen/lock.sh
```

Do not leave both commands bound to the same shortcut. Qylock terminates other
lock programs before starting, so launching both is unreliable. DMS currently
stores its generated `Super+Alt+L` binding in
`~/.config/hypr/dms/binds.lua`; re-check the binding after running `dms setup`
or regenerating DMS files.

## Update

Update the AUR development build and the rest of CachyOS:

```bash
paru -Syu
```

Update and rebuild DSearch from its source checkout:

```bash
git -C "$HOME/Documents/github/danksearch" pull --ff-only
cd "$HOME/Documents/github/danksearch"
make && sudo make install && make install-service
systemctl --user restart dsearch.service
```

Update Qylock and redeploy the chosen theme so changes reach SDDM:

```bash
git -C "$HOME/Documents/github/qylock" pull --ff-only
cd "$HOME/Documents/github/qylock"
./sddm.sh
```

If using Qylock as the desktop lockscreen, rerun `./quickshell.sh` too.

## Verification

```bash
# Development package, compositor, and session manager
pacman -Q dms-shell-git hyprland uwsm quickshell

# Source-built DSearch and its user service
dsearch version
systemctl --user is-enabled dsearch.service
systemctl --user is-active dsearch.service

# Confirm the stable DMS payload is not installed
pacman -Q dms-shell 2>/dev/null || echo "Stable dms-shell is not installed"

# Greeter and selected theme
systemctl is-enabled sddm.service
grep '^Current=' /etc/sddm.conf.d/theme.conf

# DMS service and Hyprland target
systemctl --user is-active dms.service
systemctl --user list-dependencies hyprland-session.target --plain

# Confirm the UWSM session entry exists
grep -E '^(Name|Exec)=' /usr/share/wayland-sessions/hyprland-uwsm.desktop

# DMS logs from the current boot
journalctl --user -u dms.service -b --no-pager
```

## Resources

- [DMS installation](https://danklinux.com/docs/dankmaterialshell/installation)
- [DMS keybinds and IPC](https://danklinux.com/docs/dankmaterialshell/keybinds-ipc)
- [Managing DMS](https://danklinux.com/docs/dankmaterialshell/managing)
- [DSearch](https://github.com/AvengeMedia/danksearch)
- [Hyprland with UWSM](https://wiki.hypr.land/Useful-Utilities/Systemd-start/)
- [Qylock](https://github.com/Darkkal44/qylock)
- [SDDM - ArchWiki](https://wiki.archlinux.org/title/SDDM)
