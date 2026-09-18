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
cp -r /etc/skel/.config/ ~/.config/
```

## 5. (Optional) CachyOS “Emerald” look

```bash
sudo pacman -S cachyos-emerald-kde-theme-git qogir-icon-theme
```

Then apply them in **Appearance & Style → Colors & Themes**.

---

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
