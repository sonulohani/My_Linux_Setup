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
zsh uidmap python3-virtualenv preload cgroupfs-mount mc
```

### Clang compiler
```
sudo apt install -y clang-format clang-tidy clang-tools clang clangd libc++-dev libc++1 \
libc++abi-dev libc++abi1 libclang-dev libclang1 liblldb-dev libllvm-ocaml-dev libomp-dev \
libomp5 lld lldb llvm-dev llvm-runtime llvm python3-clang
```

### Homebrew installation

```
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

### Homebrew Pakages
```
brew install lazygit fastfetch ripgrep fd aria2 bat neovim ranger trash-cli
```

### Installing essential packages (Arch Linux)
```
sudo pacman -S --needed base-devel binutils cmake extra-cmake-modules fd ripgrep gdb clang lld lldb git htop xclip meld curl wget mesa meson ninja vlc mpv ffmpeg gimp qt6 qtcreator aria2 zsh tmux gnome-terminal neovim papirus-icon-theme btop pinta podman distrobox intel-ucode gufw thunar catfish thunar-archive-plugin xarchiver
```

### Make thunar default file manager
```
xdg-mime default thunar.desktop inode/directory
```

### Thunar - Configure open in terminal 
https://askubuntu.com/a/1462901

### Chaotic AUR
https://aur.chaotic.cx/

### From Chaotic AUR
```
sudo pacman -S timeshift-autosnap pamac-aur bibata-cursor-theme nomacs microsoft-edge-stable-bin visual-studio-code-bin yay fastfetch oh-my-posh
```

### Installing packages from AUR
```
yay -Syu timeshift-systemd-timer chrome-gnome-shell
```

### For Microsoft surface laptop
```
sudo pacman -S linux-firmware-marvell
```

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

### Install kitty
```
curl -L https://sw.kovidgoyal.net/kitty/installer.sh | sh /dev/stdin
sudo ln -snf $HOME/.local/kitty.app/bin/kitty /usr/local/bin/
sudo ln -snf $HOME/.local/kitty.app/bin/kitten /usr/local/bin/ 
```

### Gnome packages / Tweaks (Ubuntu)
```
gsettings set org.gnome.mutter center-new-windows true
gsettings set org.gnome.shell.extensions.dash-to-dock click-action 'minimize'
gsettings set org.gnome.nautilus.preferences open-folder-on-dnd-hover true
sudo apt install gnome-tweaks gnome-shell-extensions
gsettings set org.gnome.desktop.sound allow-volume-above-100-percent true
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

### Installing starship
```
curl -sS https://starship.rs/install.sh | sh
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
### Superfile

```
bash -c "$(curl -sLo- https://superfile.netlify.app/install.sh)"
```

### Distrobox
```
curl -s https://raw.githubusercontent.com/89luca89/distrobox/main/install | sh -s -- --next --prefix ~/.local
```
### Zellij
https://zellij.dev/

### fzf
```
git clone --depth 1 https://github.com/junegunn/fzf.git ~/.fzf
~/.fzf/install
```

### Timeshift backup utility
```
yay -S timeshift timeshift-autosnap grub-btrfs inotify-tools
```

#### Configure backup
```
sudo systemctl edit --full grub-btrfsd # Change to this "ExecStart=/usr/bin/grub-btrfsd --syslog --timeshift-auto"
sudo systemctl enable grub-btrfsd && sudo systemctl start grub-btrfsd
```

More on this: https://www.youtube.com/watch?v=V1wxgWU0j0E

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

### PDF arranger

(Download link)[https://flathub.org/apps/com.github.jeromerobert.pdfarranger]

### Patching Nerd fonts
```
for FONT in static/*; do fontforge -script font-patcher --complete --makegroup 0 $FONT; done
```

### Add custom share folder
```
echo export 'XDG_DATA_DIRS="/opt/myapp/share:$XDG_DATA_DIRS"' >> ~/.xsessionrc
```

Taken from: https://unix.stackexchange.com/questions/471327/whats-the-right-way-to-add-directories-to-xdg-data-dirs

# Docker: Non Shared Mounts
https://github.com/89luca89/distrobox/blob/main/docs/compatibility.md#non-shared-mounts

### Drawpile

[Download link](https://github.com/drawpile/drawpile)
