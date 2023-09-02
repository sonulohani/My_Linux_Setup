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
libtool libtool-bin autoconf automake pkg-config unzip fonts-hack-ttf \
neofetch silversearcher-ag aria2 ffmpeg nomacs mpv \
clang-format clang-tidy clang-tools clang clangd libc++-dev libc++1 \
libc++abi-dev libc++abi1 libclang-dev libclang1 liblldb-dev libllvm-ocaml-dev libomp-dev \
libomp5 lld lldb llvm-dev llvm-runtime llvm python3-clang zsh uidmap python3-virtualenv tmux preload \
ripgrep fd-find
```

### Installing essential packages (Arch Linux)
```
sudo pacman -S --needed base-devel binutils cmake extra-cmake-modules fd ripgrep gdb clang lld lldb git htop xclip meld curl wget mesa meson ninja vlc mpv ffmpeg gimp qt6 qtcreator neofetch aria2 zsh tmux gnome-terminal neovim 
```

### Install wezterm
[Wezterm link](https://wezfurlong.org/wezterm/install/linux.html#installing-on-ubuntu-and-debian-based-systems)

### Gnome packages / Tweaks (Ubuntu)
```
gsettings set org.gnome.mutter center-new-windows true
gsettings set org.gnome.shell.extensions.dash-to-dock click-action 'minimize'
gsettings set org.gnome.nautilus.preferences open-folder-on-dnd-hover true
sudo apt install gnome-tweaks gnome-shell-extensions
```

### Gnome packages / Tweaks (Arch Linux)
```
gsettings set org.gnome.mutter center-new-windows true
gsettings set org.gnome.shell.extensions.dash-to-dock click-action 'minimize'
gsettings set org.gnome.nautilus.preferences open-folder-on-dnd-hover true
sudo pacman -S --needed gnome-tweaks gnome-browser-connector gnome-shell-extensions
```

### Yay packages
```
yay timeshift visual-studio-code-bin google-chrome
```

### Lazy vim
#### If neovim config is present in the system
```
# required
rm -rf ~/.config/nvim
rm -rf ~/.local/share/nvim
rm -rf ~/.local/state/nvim
rm -rf ~/.cache/nvim
```
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

### Tmux
```
cd
git clone https://github.com/gpakosz/.tmux.git
ln -s -f .tmux/.tmux.conf
cp .tmux/.tmux.conf.local .
```

### Add these config 
```
nvim .tmux.conf
set -g mouse on
set -ga terminal-overrides ',*256color*:smcup@:rmcup@'
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

```
sed -i 's/plugins=(git)/plugins=(git zsh-autosuggestions zsh-syntax-highlighting emoji emotty)/g' ~/.zshrc
```

### Distrobox
```
curl -s https://raw.githubusercontent.com/89luca89/distrobox/main/install | sh -s -- --next --prefix ~/.local
```

### Fonts
1. [Nerd fonts](https://www.nerdfonts.com/font-downloads)
2. [Fira code](https://github.com/tonsky/FiraCode)

### Deb softwares
1. [Google chrome](https://www.google.com/intl/en_in/chrome/)
2. [VS Code](https://code.visualstudio.com/)
3. [Edge](https://www.microsoft.com/en-gb/edge)

## Optional

### Arch linux container
```
sudo pacman -S gdb clang lldb lld qtcreator qt6 ffmpeg mpv vlc neovim cmake extra-cmake-modules gimp mesa htop neofetch python curl wget ninja meson the_silver_searcher aria2 unzip git base-devel pcmanfm gnome-terminal gnome-text-editor python-pip rust xclip
```

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
#### Removing unnecessary packages
```
sudo apt purge -y thunderbird gnome-mahjongg gnome-mines gnome-sudoku aisleriot
sudo apt autoremove --purge -y
```

#### Linux mint bluetooth
```
sudo systemctl enable --now bluetooth
```

### Paint Program
```
flatpak install flathub org.kde.kolourpaint
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

### Lapce text editor
https://lapce.dev/

### Podman backup and restore
https://fedoramagazine.org/backup-and-restore-toolboxes-with-podman/
