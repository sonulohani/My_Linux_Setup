Here are the commands to install KDE Plasma on CachyOS, based on the [official CachyOS KDE wiki](https://wiki.cachyos.org/configuration/desktop_environments/kde/) and current CachyOS defaults (Plasma Login Manager instead of SDDM).

---

## 1. Update the system first

```bash
sudo pacman -Syu
```

---

## 2. Install KDE Plasma (core)

```bash
sudo pacman -S plasma-meta plasma-login-manager cachyos-kde-settings kde-applications drawy
```

When `pacman` asks about providers (fonts, multimedia, etc.), press **Enter** to accept defaults unless you have a preference.

---

## 3. Enable the display manager

```bash
sudo systemctl enable plasmalogin.service
```

---

## 4. Copy cachy os config to home folder

```bash
cp -r /etc/skel/.config/ ~/.config/a
```

## 5. (Optional) CachyOS “Emerald” look

```bash
sudo pacman -S cachyos-emerald-kde-theme-git qogir-icon-theme
```

Then apply them in **Appearance & Style → Colors & Themes**.

---