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
sudo pacman -Syu cachyos-hypr-noctalia foot
```

If you use `paru`, the equivalent command is:

```bash
paru -Syu cachyos-hypr-noctalia foot
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

### All commands at single shot

```bash
paru -Syu brave udiskie udisks2 cachyos-hypr-noctalia hyprland noctalia uwsm foot \
  xdg-desktop-portal xdg-desktop-portal-hyprland xdg-desktop-portal-gtk \
  matugen cliphist wl-clipboard grim slurp qt6ct qt5ct gnome-keyring \
  nautilus qt6-declarative qt6-5compat qt6-svg qt6-multimedia qt6-multimedia-ffmpeg \
  gst-plugins-base gst-plugins-good gst-plugins-bad gst-plugins-ugly gnome-console \
  sddm ddcutil playerctl power-profiles-daemon upower snappy-switcher kitty zed hyprmod hyprpm pyprland swash --needed
```

### Hyprland plagins

```bash
hyprpm add https://github.com/hyprwm/hyprland-plugins
```

#### Hypr dynamic cursors

```bash
hyprpm add https://github.com/virtcode/hypr-dynamic-cursors
hyprpm enable dynamic-cursors
```

#### Hyprglass

```bash
hyprpm add https://github.com/hyprnux/hyprglass
hyprpm enable hyprglass
```

#### To update plugins

```bash
 hyprpm update -f
hyprpm reload
```

### For performance
```bash
powerprofilesctl set performance
sudo x86_energy_perf_policy --all performance
sudo cpupower -c all frequency-set -g performance
sudo pacman -S --needed thermald
sudo systemctl enable --now thermald
```

For setting forcefully

```bash
for f in /sys/devices/system/cpu/cpu*/cpufreq/energy_performance_preference; do
    echo performance | sudo tee "$f" >/dev/null
done
```

## TLP

### 1. Install TLP

```bash
sudo pacman -S tlp tlp-pd
```

`tlp-pd` is useful because it provides the Power Profiles Daemon compatibility interface, including desktop profile switching. CachyOS packages it as a replacement for `power-profiles-daemon`. ([CachyOS Package Dashboard][2])

### 2. Make sure `power-profiles-daemon` isn't fighting TLP

TLP and `power-profiles-daemon` are conflicting power-management systems. ([Arch Wiki][3])

Check:

```bash
systemctl status power-profiles-daemon
```

If it's installed/running:

```bash
sudo systemctl disable --now power-profiles-daemon.service
sudo systemctl mask power-profiles-daemon.service
```

Because `tlp-pd` provides `power-profiles-daemon`, installing `tlp-pd` may already handle the package side of this for you. ([CachyOS Package Dashboard][2])

You can verify:

```bash
pacman -Qs power-profiles-daemon
pacman -Qs tlp
```

### 3. Enable TLP

```bash
sudo systemctl enable --now tlp.service
sudo systemctl enable --now tlp-pd.service
```

TLP specifically requires `tlp.service`; `tlp-pd.service` is needed for desktop profile switching. ([TLP Documentation][4])

### 4. Configure performance mode

TLP 1.9+ has three profiles:

* `performance`
* `balanced`
* `power-saver`

On the current TLP configuration model, the `_AC` settings belong to the performance profile. ([TLP Documentation][5])

Create a small override instead of editing the giant main config:

```bash
sudo mkdir -p /etc/tlp.d
sudo nano /etc/tlp.d/01-performance.conf
```

Put:

```ini
# CPU energy/performance preference
CPU_ENERGY_PERF_POLICY_ON_AC=performance

# Keep turbo/boost enabled
CPU_BOOST_ON_AC=1
CPU_HWP_DYN_BOOST_ON_AC=1

# Firmware/platform performance profile
PLATFORM_PROFILE_ON_AC=performance
```

TLP documents `CPU_ENERGY_PERF_POLICY_ON_AC=performance` specifically as the setting for maximum CPU performance on AC, while `PLATFORM_PROFILE_ON_AC=performance` selects the firmware's performance-oriented platform mode. ([TLP Documentation][6])

### 5. Apply it

Don't restart the systemd service just to apply configuration. TLP recommends:

```bash
sudo tlp start
```

([TLP Documentation][7])

Then explicitly select performance:

```bash
sudo tlp performance
```

Or, with `tlp-pd`:

```bash
tlpctl performance
```

`tlpctl` does not require root. ([TLP Documentation][8])

### 6. Verify EPP

This is the important part given the EPP issue you were hitting earlier.

Run:

```bash
sudo tlp-stat -p
```

You want to see something along the lines of:

```text
scaling_driver = intel_pstate
...
energy_performance_preference = performance [EPP]
```

TLP's processor diagnostics are specifically designed to show the active scaling driver and EPP state. ([TLP Documentation][9])

You can also check directly:

```bash
cat /sys/devices/system/cpu/cpu0/cpufreq/energy_performance_preference
```

Expected:

```text
performance
```

And all CPUs:

```bash
grep . /sys/devices/system/cpu/cpu*/cpufreq/energy_performance_preference
```

### One important thing about your earlier `cpupower` error

You previously got:

```text
Device or resource busy
Error setting epp value on CPU 0
```

That's very likely because something else was already controlling the CPU policy. With TLP installed, **don't fight it with `cpupower set --epp performance`**. Let TLP own the setting.

TLP's own documentation also notes that with `intel_pstate`/`amd-pstate` in active mode, the governor and EPP interact: using the `performance` governor effectively locks EPP to `performance`. ([TLP Documentation][10])

### 7. Check the complete state

Run:

```bash
tlp-stat -s
echo
tlp-stat -p
echo
tlpctl get
```

You ideally want:

```text
TLP = enabled
tlp-pd = enabled, running
TLP profile = performance
```

and:

```text
energy_performance_preference = performance
```

### About battery

I'd **not** force performance on battery. Keep:

```ini
CPU_ENERGY_PERF_POLICY_ON_BAT=balance_power
```

or simply leave the TLP default. TLP's normal defaults are performance on AC and increasingly power-conscious profiles on battery. ([TLP Documentation][11])

So the clean setup for your CachyOS laptop is essentially:

```text
AC:
    TLP performance
    EPP = performance
    platform profile = performance
    turbo/boost = enabled

Battery:
    TLP balanced
    EPP = balance_power
```

And **don't run `power-profiles-daemon` alongside TLP**. `tlp-pd` is the compatibility layer you want instead. ([CachyOS Package Dashboard][2])

One caveat: if you're using **CachyOS's `scx_loader`**, CachyOS deliberately integrates its power profiles with scheduler profiles; its `Performance` profile maps to the `Gaming` scheduler profile. Switching to TLP means you should check whether you still want that particular CachyOS integration. ([CachyOS][12])

For your machine, I'd actually check `tlp-stat -p` next—especially the **scaling driver (`intel_pstate`), governor, EPP, platform profile, and boost state**—because that will tell us whether TLP is truly giving you full performance rather than just saying "performance" on the surface.

[1]: https://packages.cachyos.org/package/extra/any/tlp?utm_source=chatgpt.com "CachyOS | tlp - extra (any)"
[2]: https://packages.cachyos.org/package/extra/any/tlp-pd?utm_source=chatgpt.com "CachyOS | tlp-pd - extra (any)"
[3]: https://wiki.archlinux.org/title/CPU_frequency_scaling?source=your_stories_page---------------------------&utm_source=chatgpt.com "CPU frequency scaling - ArchWiki"
[4]: https://linrunner.de/tlp/installation/arch.html?utm_source=chatgpt.com "Arch Linux — TLP 1.10.2 documentation"
[5]: https://linrunner.de/tlp/usage/index.html?utm_source=chatgpt.com "Usage — TLP 1.10.2 documentation"
[6]: https://linrunner.de/tlp/support/optimizing.html?utm_source=chatgpt.com "Optimizing Guide — TLP 1.10.2 documentation"
[7]: https://linrunner.de/tlp/usage/tlp.html?utm_source=chatgpt.com "tlp — TLP 1.10.2 documentation"
[8]: https://linrunner.de/tlp/usage/tlpctl.html?utm_source=chatgpt.com "tlpctl — TLP 1.10.2 documentation"
[9]: https://linrunner.de/tlp/usage/tlp-stat.html?utm_source=chatgpt.com "tlp-stat — TLP 1.10.2 documentation"
[10]: https://linrunner.de/tlp/faq/processor.html?utm_source=chatgpt.com "Processor — TLP 1.10.2 documentation"
[11]: https://linrunner.de/tlp/settings/introduction.html?utm_source=chatgpt.com "Introduction — TLP 1.10.2 documentation"
[12]: https://wiki.cachyos.org/configuration/sched-ext/?utm_source=chatgpt.com "sched-ext Tutorial | CachyOS"

### Install Nemo

```bash
sudo pacman -S --needed \
    nemo \
    nemo-fileroller \
    nemo-image-converter \
    nemo-compare \
    nemo-emblems \
    nemo-media-columns \
    nemo-terminal \
    nemo-audio-tab \
    nemo-pastebin \
    nemo-repairer \
    nemo-share \
    gvfs \
    gvfs-smb \
    gvfs-mtp \
    gvfs-gphoto2 \
    gvfs-dnssd \
    udisks2 \
    polkit-gnome \
    tumbler \
    ffmpegthumbnailer \
    poppler-glib \
    libgsf \
    freetype2 \
    webp-pixbuf-loader \
    file-roller \
    p7zip \
    unzip \
    unrar bulky
```

```bash
xdg-mime default nemo.desktop inode/directory
```

Use bulky for renaming multiple files.

#### For open in terminal defaults

```bash
gsettings set org.cinnamon.desktop.default-applications.terminal exec 'foot'
nemo -q
```

## Sources

- [CachyOS Hyprland post-install guide](https://wiki.cachyos.org/configuration/desktop_environments/hyprland/)
- [Noctalia v5 installation guide](https://docs.noctalia.dev/noctalia/getting-started/installation/)
- [CachyOS Hyprland/Noctalia settings package](https://dashboard.cachyos.org/package/cachyos/any/cachyos-hypr-noctalia)
- [CachyOS Hyprland/Noctalia configuration repository](https://github.com/CachyOS/cachyos-hypr-noctalia)
- [Hypr dynamic cursors](https://github.com/VirtCode/hypr-dynamic-cursors)
- [Hyprglass](https://github.com/hyprnux/hyprglass)
