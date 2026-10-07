# KDE Plasma Customization

## Installation

Install the active repository packages:

```bash
paru -S --needed \
    kdeplasma-addons \
    breeze \
    breeze-icons \
    breeze-cursors \
    inter-font \
    plasma6-applets-panel-colorizer \
    kwin-effects-better-blur-dx \
    kwin-effects-glass-git \
    vicinae
```

```bash
systemctl --user enable --now vicinae.service
```

Install the active foreign/AUR packages:

```bash
paru -S --needed \
    darkly \
    kde-material-you-colors-git \
    plasma6-applets-wallpaper-effects \
    kwin-effect-rounded-corners-git \
    vinyl \
    klassy
```

Install the optional packages that are present but inactive:

```bash
paru -S --needed \
    cachyos-kde-settings \
    cachyos-iridescent-kde \
    cachyos-nord-kde-theme-git \
    cachyos-emerald-kde-theme-git \
    cachyos-wallpapers \
    bibata-cursor-theme \
    plasma6-applets-audio-visualizer \
    tela-icon-theme
```

Modern Clock, Ant-Dark, Maple Mono NF, Tela icons, and Vector Clock need to be
restored separately from their upstream sources or from Plasma's **Get New
Widgets/Themes** interface.

### KWin Scripts

#### [KClear](https://github.com/AaronRohrbacher/klear_kwin)

##### Fix KClear Without Reinstalling

First, verify that KClear is installed:

```bash
ls -la ~/.local/share/kwin/scripts/klear/
```

The directory should contain files similar to these:

```text
build-applist.sh
klear-applist.service
klear-applist.path
contents/
metadata.json
```

If these files exist, link the systemd user units and enable the path unit:

```bash
mkdir -p ~/.config/systemd/user

ln -sfn ~/.local/share/kwin/scripts/klear/klear-applist.service \
    ~/.config/systemd/user/klear-applist.service

ln -sfn ~/.local/share/kwin/scripts/klear/klear-applist.path \
    ~/.config/systemd/user/klear-applist.path

systemctl --user daemon-reload
systemctl --user enable --now klear-applist.path
```

Finally, force KClear to generate the application list:

```bash
KLEAR_FORCE=1 ~/.local/share/kwin/scripts/klear/build-applist.sh
```

#### [KZones](https://github.com/gerritdevriese/kzones)

### Plasma Styles

* Apple-Dark
* Ant-Dark
* Layan look and feel theme
* Dream-Dark-Color-Global-6
* Nordic-bluish
* Nordic

### Widgets

* Modern Clock

### Icon Theme

* [Tela Icon Theme](https://github.com/vinceliuice/Tela-icon-theme)
