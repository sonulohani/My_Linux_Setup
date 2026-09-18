# KDE Plasma Customization

## Installation

Install the active repository packages:

```bash
sudo pacman -S --needed \
  kdeplasma-addons breeze breeze-icons breeze-cursors inter-font plasma6-applets-panel-colorizer
```

Install the active foreign/AUR packages:

```bash
paru -S --needed \
  darkly \
  kde-material-you-colors-git \
  plasma6-applets-wallpaper-effects kwin-effect-rounded-corners-git vinyl
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

### Kwin script

* [KClear](https://github.com/AaronRohrbacher/klear_kwin)

### Plasma Style

* Apple-Dark
* Ant-Dark

### Widgets

* Mordern Clock

### Icon theme

* [Tela Icon Theme](https://github.com/vinceliuice/Tela-icon-theme)

### All changes with one command

Go to : https://github.com/ladybug-me/caelestia-dots-kde
