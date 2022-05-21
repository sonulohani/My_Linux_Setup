#!/usr/bin/env bash

set -eu

SCRIPT_DIR=$(pwd)

cd ${HOME}

echo "Removing unnecessary packages"
sudo apt purge -y thunderbird gnome-mahjongg gnome-mines gnome-sudoku aisleriot
sudo apt autoremove --purge -y

# Fsearch
sudo add-apt-repository ppa:christian-boxdoerfer/fsearch-stable

echo "Updating the system"
sudo apt update && sudo apt upgrade -y

echo "Installing essential packages"
sudo apt install -y python3-pip build-essential binutils neovim cmake-qt-gui \
gufw g++ gdb git ubuntu-restricted-extras rar unrar p7zip-full p7zip-rar neofetch \
htop silversearcher-ag xclip meld obs-studio apt-transport-https curl gnome-tweaks \
gnome-shell-extensions wget network-manager-openvpn-gnome extra-cmake-modules timeshift \
mesa-common-dev libglu1-mesa-dev vlc flatpak gimp zsh ninja-build gettext \
libtool libtool-bin autoconf automake cmake g++ pkg-config unzip fsearch fonts-hack-ttf \ 
gnome-text-editor

# echo "Installing optional packages"
# sudo apt install -y dconf-editor timeshift terminator snapd flatpak gimp qt5-default zsh 
# sudo apt install ninja-build gettext libtool libtool-bin autoconf automake cmake g++ pkg-config unzip

# Clang
https://apt.llvm.org/

# Fonts
https://github.com/tonsky/FiraCode
https://github.com/adobe-fonts/source-code-pro
https://www.nerdfonts.com/font-downloads
https://github.com/i-tu/Hasklig
https://rubjo.github.io/victor-mono/

# Configure flathub
flatpak remote-add --if-not-exists flathub https://flathub.org/repo/flathub.flatpakrepo

echo "Configure git username/email"
git config --global user.name "Sonu Lohani"
git config --global user.email "sonulohani@gmail.com"
git config --global merge.tool meld
git config --global diff.tool meld

echo "Installing Spacevim"
curl -sLf https://spacevim.org/install.sh | bash

echo "Enabling firewall"
sudo systemctl enable ufw

echo "Setting ssh"
ssh-keygen -t rsa -b 4096 -C "sonulohani@gmail.com"
eval "$(ssh-agent -s)"
ssh-add ${HOME}/.ssh/id_rsa

echo "Install ohmyzsh"
cd ${HOME}
sh -c "$(curl -fsSL https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)"

echo "Installing zsh-autosuggestions"
git clone https://github.com/zsh-users/zsh-autosuggestions ${ZSH_CUSTOM:-~/.oh-my-zsh/custom}/plugins/zsh-autosuggestions

echo "Installing zsh-syntax-highlighting"
git clone https://github.com/zsh-users/zsh-syntax-highlighting.git ${ZSH_CUSTOM:-~/.oh-my-zsh/custom}/plugins/zsh-syntax-highlighting

echo "Installing powerlevel10k"
git clone --depth=1 https://github.com/romkatv/powerlevel10k.git ${ZSH_CUSTOM:-$HOME/.oh-my-zsh/custom}/themes/powerlevel10k

# ZSH Manually setup----------------------------------------------------
# ZSH_THEME="powerlevel10k/powerlevel10k"
# plugins=(git zsh-autosuggestions zsh-syntax-highlighting)
# My changes begin                                                              
# export PATH=${HOME}/Programs:$PATH                                          
# My changes end  
#------------------------------------------------------------------------

# Extra
# Install chrome
# Install code
# Install virtualbox
# Install PlugInstall
# Install k2pdfopt, openshot, mypaint, inkscape
# change font in terminator and gnome-terminal
# Extensions: Caffeine, clipboard indicator, dash to dock(enable trash and click to minimize), blyr, TopIcon Plus, Desktop Icons NG(DING), KStatusNotifierItem/AppIndicator Support
# Pop Shell, https://extensions.gnome.org/extension/1238/time/, Night theme switcher, Removable driver menu, https://extensions.gnome.org/extension/1262/bing-wallpaper-changer/, https://extensions.gnome.org/extension/4269/alphabetical-app-grid/
# xclip -sel clip < ~/.ssh/id_rsa.pub
# Install FireDM download manager

# peek
# https://github.com/phw/peek

# For terminal themes
# bash -c  "$(wget -qO- https://git.io/vQgMr)"

# Install Joplin
# https://joplinapp.org/
