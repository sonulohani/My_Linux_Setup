Here are the commands to install KDE Plasma on CachyOS, based on the [official CachyOS KDE wiki](https://wiki.cachyos.org/configuration/desktop_environments/kde/) and current CachyOS defaults (Plasma Login Manager instead of SDDM).

---

## 1. Update the system first

```bash
sudo pacman -Syu
```

---

## 2. Install KDE Plasma (core)

```bash
sudo pacman -S plasma-meta plasma-login-manager
```

When `pacman` asks about providers (fonts, multimedia, etc.), press **Enter** to accept defaults unless you have a preference.

---

## 3. Enable the display manager

```bash
sudo systemctl enable plasmalogin.service
```

---

## 4. (Recommended) CachyOS KDE tweaks

```bash
sudo pacman -S cachyos-kde-settings
```

---

## 5. (Optional) Full KDE application suite

```bash
sudo pacman -S kde-applications
```

Or install only what you need, e.g.:

```bash
sudo pacman -S dolphin konsole kate gwenview ark spectacle
```

---

## 6. (Optional) CachyOS “Emerald” look

```bash
sudo pacman -S cachyos-emerald-kde-theme-git qogir-icon-theme
```

Then apply them in **Appearance & Style → Colors & Themes**.

---

## 7. Reboot

```bash
sudo reboot
```

At the login screen, choose **Plasma (Wayland)** or **Plasma (X11)** if you installed X11.

---