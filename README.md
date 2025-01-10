### Updating the system
```
sudo apt update && sudo apt upgrade
```

### Installing essential packages (Ubuntu)
```
sudo apt install -y python3-pip build-essential binutils cmake-qt-gui \
g++ gdb git rar unrar p7zip-full p7zip-rar fonts-dejavu \
htop xclip meld curl wget extra-cmake-modules \
mesa-common-dev libglu1-mesa-dev vlc flatpak gimp gettext ninja-build \
libtool libtool-bin autoconf automake pkg-config unzip fonts-hack-ttf ffmpeg nomacs mpv \
zsh python3-virtualenv preload mc
```

### Homebrew installation

```
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

### Homebrew Pakages
```
brew install lazygit fastfetch ripgrep fd aria2 bat neovim ranger trash-cli hwatch
```

### Chaotic AUR
https://aur.chaotic.cx/

### Enable fstrim.timer
```
sudo systemctl enable fstrim.timer && sudo systemctl start fstrim.timer
```

### Enable ufw
```
sudo ufw enable
```

### Install wezterm
[Wezterm link](https://wezfurlong.org/wezterm/install/linux.html#installing-on-ubuntu-and-debian-based-systems)

### Gnome packages / Tweaks (Ubuntu)
```
gsettings set org.gnome.mutter center-new-windows true
gsettings set org.gnome.shell.extensions.dash-to-dock click-action 'minimize'
gsettings set org.gnome.nautilus.preferences open-folder-on-dnd-hover true
sudo apt install gnome-tweaks gnome-shell-extensions
gsettings set org.gnome.desktop.sound allow-volume-above-100-percent true
```

### Lazy vim
#### If neovim config is present in the system
```
git clone https://github.com/LazyVim/starter ~/.config/nvim
rm -rf ~/.config/nvim/.git
```

### Snap refresh
```
sudo snap refresh
```

### Configure flathub
```
flatpak remote-add --if-not-exists flathub https://flathub.org/repo/flathub.flatpakrepo
```

### Configure git username/email
```
git config --global user.name "Sonu Lohani"
git config --global user.email "sonulohani@gmail.com"
git config --global merge.tool meld
git config --global diff.tool meld
```

### Install ohmyzsh
```
sh -c "$(curl -fsSL https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)"
```

### Installing zsh-autosuggestions
```
git clone https://github.com/zsh-users/zsh-autosuggestions ${ZSH_CUSTOM:-~/.oh-my-zsh/custom}/plugins/zsh-autosuggestions
```

### Installing zsh-syntax-highlighting
```
git clone https://github.com/zsh-users/zsh-syntax-highlighting.git ${ZSH_CUSTOM:-~/.oh-my-zsh/custom}/plugins/zsh-syntax-highlighting
```

### Installing you-should-use
```
git clone https://github.com/MichaelAquilina/zsh-you-should-use.git $ZSH_CUSTOM/plugins/you-should-use
```

### Installing zsh-safe-rm
```
git clone --recursive --depth 1 https://github.com/mattmc3/zsh-safe-rm.git ${ZSH_CUSTOM:-~/.oh-my-zsh/custom}/plugins/zsh-safe-rm
```

```
sed -i 's/plugins=(git)/plugins=(git zsh-autosuggestions zsh-syntax-highlighting you-should-use zsh-safe-rm emoji emotty)/g' ~/.zshrc
```

### Atuin

```
curl --proto '=https' --tlsv1.2 -LsSf https://setup.atuin.sh | sh
```

### Installing wezterm

```
curl -fsSL https://apt.fury.io/wez/gpg.key | sudo gpg --yes --dearmor -o /usr/share/keyrings/wezterm-fury.gpg
echo 'deb [signed-by=/usr/share/keyrings/wezterm-fury.gpg] https://apt.fury.io/wez/ * *' | sudo tee /etc/apt/sources.list.d/wezterm.list
```

```
sudo apt update && sudo apt install wezterm
```

### Distrobox
```
curl -s https://raw.githubusercontent.com/89luca89/distrobox/main/install | sh -s -- --next --prefix ~/.local
```

### Zellij
https://zellij.dev/

### Deb softwares
1. [Google chrome](https://www.google.com/intl/en_in/chrome/)
2. [VS Code](https://code.visualstudio.com/)
3. [Edge](https://www.microsoft.com/en-gb/edge)

## Optional

### Installing powerlevel10k
```
git clone --depth=1 https://github.com/romkatv/powerlevel10k.git ${ZSH_CUSTOM:-$HOME/.oh-my-zsh/custom}/themes/powerlevel10k
```

<!-- To remove apt key deprecated warning due to above commands follow the instruction here: 
https://askubuntu.com/questions/1398344/apt-key-deprecation-warning-when-updating-system -->

### Installing optional packages
```
sudo apt install -y ubuntu-restricted-extras dconf-editor timeshift terminator snapd qt5-default obs-studio
```

### Extra

#### Start Bluetooth
```
sudo systemctl enable bluetooth.service && sudo systemctl start bluetooth.service 
```

### Set path for sudo commands 
https://superuser.com/a/927599

### For zram in open suse microos
```
sudo transactional-update pkg install systemd-zram-service
```
```
sudo systemctl enable zramswap --now
```
#### For other system zram config
[ZRam setup link](https://fosspost.org/enable-zram-on-linux-better-system-performance/)

### Add wezterm in nautilus context menu

https://github.com/Stunkymonkey/nautilus-open-any-terminal

###  Best gnome extension
1. https://extensions.gnome.org/extension/4412/advanced-alttab-window-switcher/
2. https://extensions.gnome.org/extension/4269/alphabetical-app-grid/
3. https://extensions.gnome.org/extension/517/caffeine/
4. https://extensions.gnome.org/extension/3396/color-picker/
5. https://extensions.gnome.org/extension/4451/logo-menu/
6. https://extensions.gnome.org/extension/19/user-themes/
7. https://extensions.gnome.org/extension/779/clipboard-indicator/
8. https://extensions.gnome.org/extension/2087/desktop-icons-ng-ding/
9. https://extensions.gnome.org/extension/615/appindicator-support/
10. https://extensions.gnome.org/extension/1460/vitals/
11. https://extensions.gnome.org/extension/3843/just-perfection/

### Show icon in dash to dock
Launch one such application, say Terminator, whose correct icon is not seen in Ubuntu Dock.
Run xprop WM_CLASS in Terminal. The cursor should turn into a crosshair.
Place the crosshair over Terminator and click. You should get a WM_CLASS string for Terminator.

Open Terminator's .desktop file and add the following line

StartupWMClass=OBTAINED-VALUE

In place of OBTAINED-VALUE put a value you got from step 3 without any quotes.

Save the .desktop file.

# Enable fractional scaling in gnome wayland
```
gsettings set org.gnome.mutter experimental-features "['scale-monitor-framebuffer']"
```

### Disk usage analyzer
```
sudo apt install baobab
```

# Docker: Non Shared Mounts
https://github.com/89luca89/distrobox/blob/main/docs/compatibility.md#non-shared-mounts

### Drawpile

[Download link](https://github.com/drawpile/drawpile)

### PDF arranger

[Download link](https://flathub.org/apps/com.github.jeromerobert.pdfarranger)

### Upsacyl
```
flatpak install flathub org.upscayl.Upscayl
```

### ExcaliDraw

[Link to access](https://github.com/excalidraw/excalidraw)
