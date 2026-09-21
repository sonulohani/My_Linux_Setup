# KDE Plasma Customization

## Installation

Install the active repository packages:

```bash
paru -S --needed \
  kdeplasma-addons breeze breeze-icons breeze-cursors \ 
  inter-font plasma6-applets-panel-colorizer kwin-effects-better-blur-dx

```

Install the active foreign/AUR packages:

```bash
paru -S --needed \
  darkly \
  kde-material-you-colors-git \
  plasma6-applets-wallpaper-effects kwin-effect-rounded-corners-git vinyl klassy
```

Install the optional packages that are present but inactive:

```bash
sudo pacman -S --needed \
  cachyos-kde-settings cachyos-iridescent-kde \
  cachyos-nord-kde-theme-git cachyos-emerald-kde-theme-git \
  cachyos-wallpapers bibata-cursor-theme plasma6-applets-audio-visualizer tela-icon-theme
```

Modern Clock, Ant-Dark, Maple Mono NF, Tela icons, and Vector Clock need to be
restored separately from their upstream sources or from Plasma's **Get New
Widgets/Themes** interface.

### Kwin script

* [KClear](https://github.com/AaronRohrbacher/klear_kwin)
* [KZones](https://github.com/gerritdevriese/kzones)

### Plasma Style

* Apple-Dark
* Ant-Dark
* Layan look and feel theme
* Dream-Dark-Color-Global-6
* Nordic-bluish
* Nordic

### Widgets

* Mordern Clock

### Icon theme

* [Tela Icon Theme](https://github.com/vinceliuice/Tela-icon-theme)

### All changes with one command

Go to : https://github.com/ladybug-me/caelestia-dots-kde
