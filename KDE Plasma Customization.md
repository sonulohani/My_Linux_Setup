# KDE Plasma Customization

This is a snapshot of the Plasma customization detected on this machine on
2026-09-07. It distinguishes the active desktop setup from packages and themes
that are installed but not currently selected.

## Active appearance

- **Global theme:** Breeze Dark (`org.kde.breezedark.desktop`)
- **Plasma style:** Ant-Dark
- **Application style:** Darkly
- **Window decoration:** Darkly
- **Color scheme:** MaterialYouDark, generated from the wallpaper
- **Icons:** Breeze Dark (CachyOS/KDE default)
- **Cursor:** Breeze
- **UI font:** Inter 10 pt
- **Monospace font:** Maple Mono NF 10 pt
- **Animation speed:** 0.25×

The active settings were found in:

- `~/.config/kdeglobals`
- `~/.config/kwinrc`
- `~/.config/plasmarc`
- `~/.config/kdedefaults/kdeglobals`
- `~/.config/kdedefaults/kcminputrc`

## Customization packages in active use

| Package | Version | Source | Purpose |
| --- | --- | --- | --- |
| `darkly` | 0.5.39-2 | Foreign/AUR-style package | Active Qt application style and KWin window decoration |
| `kde-material-you-colors-git` | 2.2.0.r6.g0b4d150-1 | AUR | Generates the active Material You color scheme from the wallpaper |
| `plasma6-applets-panel-colorizer` | 8.0.0-1 | CachyOS repository | Customizes the Plasma panel; the Transparent preset is active |
| `plasma6-applets-wallpaper-effects` | 2.1.1-1 | AUR | Enables wallpaper effects on both configured desktops |
| `inter-font` | 4.1-1 | Repository | Active Plasma interface font |
| `breeze-icons` | 6.29.0-1.1 | Repository | Active icon theme |
| `breeze-cursors` | 6.7.4-2.1 | Repository | Active cursor theme |

`kde-material-you-colors` starts automatically through
`~/.config/autostart/kde-material-you-colors.desktop`.

## Active third-party Plasma assets

These were installed in the user account rather than through Pacman.

### Modern Clock

- Plugin ID: `com.github.prayag2.modernclock`
- Version: 1.0.0
- Status: active on the desktop
- Source: <https://github.com/prayag2/kde_modernclock>
- Location: `~/.local/share/plasma/plasmoids/com.github.prayag2.modernclock`

### Ant-Dark Plasma style

- Version: 1.0.0
- Author: EliverLara
- Status: active
- Source: <https://github.com/EliverLara/Ant/tree/master/kde/Dark>
- Location: `~/.local/share/plasma/desktoptheme/Ant-Dark`

### Maple Mono NF

- Status: active as the fixed-width font
- Installation: manually installed, not owned by a Pacman package
- Location: `~/.local/share/fonts/MapleMono-NF-unhinted`

## Active panel and desktop widgets

The customized panel contains:

- Application Launcher
- Pager
- Icons-Only Task Manager
- Digital Clock
- System Tray
- Show Desktop
- Panel Colorizer

The desktop contains:

- Modern Clock
- Wallpaper Effects on both displays

The active wallpapers are:

- `~/Pictures/Wallpapers/0132.jpg`
- `~/Pictures/Wallpapers/a_group_of_people_with_umbrellas_walking_in_the_rain.png`

## Active KWin effects

These built-in KWin effects are enabled:

- Blur, with increased saturation
- Fall Apart
- Mouse Mark
- Sheet
- Translucency
- Wobbly Windows
- Night Color

The desktop also uses a three-column tiling layout with 4 px padding and
25% / 50% / 25% column widths.

## Installed but not currently active

The following customization packages or assets are installed, but they do not
appear in the current panel/desktop layout or active theme settings:

| Item | Version/source | Notes |
| --- | --- | --- |
| `plasma6-applets-audio-visualizer` | 3.6.1-1, AUR | Installed explicitly; not present in the active layout |
| Vector Clock | 1.0.2, KDE Store | User plasmoid installed but not active |
| `cachyos-iridescent-kde` | r2.16aa352-1 | Alternative CachyOS KDE theme |
| `cachyos-nord-kde-theme-git` | r17.d1fb6a7-1 | Alternative CachyOS Nord theme |
| `cachyos-emerald-kde-theme-git` | r25.d61d1dd-1 | Alternative CachyOS Emerald theme |
| `bibata-cursor-theme` | 2.0.7-1.1 | Installed, but Breeze is selected |
| Tela icon themes | Manual installation | Many variants are installed under `~/.local/share/icons`, but Breeze Dark is selected |
| `cachyos-wallpapers` | r23.964263e-1 | Installed; current desktops use personal wallpaper files |

Vector Clock source: <https://store.kde.org/p/2137726/>

## Reinstallation

Install the active repository packages:

```bash
sudo pacman -S --needed \
  plasma-desktop plasma-workspace kwin kdeplasma-addons \
  breeze breeze-icons breeze-cursors inter-font \
  plasma6-applets-panel-colorizer
```

Install the active foreign/AUR packages:

```bash
paru -S --needed \
  darkly \
  kde-material-you-colors-git \
  plasma6-applets-wallpaper-effects
```

Install the optional packages that are present but inactive:

```bash
sudo pacman -S --needed \
  cachyos-kde-settings cachyos-iridescent-kde \
  cachyos-nord-kde-theme-git cachyos-emerald-kde-theme-git \
  cachyos-wallpapers bibata-cursor-theme

paru -S --needed plasma6-applets-audio-visualizer
```

Modern Clock, Ant-Dark, Maple Mono NF, Tela icons, and Vector Clock need to be
restored separately from their upstream sources or from Plasma's **Get New
Widgets/Themes** interface.

## Configuration files worth backing up

Package installation alone will not reproduce the layout. Back up these files
and directories as well:

```text
~/.config/kdeglobals
~/.config/kwinrc
~/.config/plasmarc
~/.config/plasma-org.kde.plasma.desktop-appletsrc
~/.config/autostart/kde-material-you-colors.desktop
~/.local/share/plasma/plasmoids/
~/.local/share/plasma/desktoptheme/Ant-Dark/
~/.local/share/color-schemes/MaterialYou*.colors
~/.local/share/fonts/MapleMono-NF-unhinted/
```

The package versions above are a point-in-time inventory. Use package names,
not pinned versions, when recreating the setup on an updated CachyOS system.

### All changes with one command

Go to : https://github.com/ladybug-me/caelestia-dots-kde
