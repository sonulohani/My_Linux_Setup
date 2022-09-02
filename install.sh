#!/usr/bin/env bash

set -eu

SCRIPT_DIR=$(pwd)

sudo apt install -y timeshift

echo "Updating the system"
sudo apt update && sudo apt upgrade -y

echo "Installing essential packages"
sudo apt install -y python3-pip build-essential binutils cmake-qt-gui \
gufw g++ gdb git rar unrar p7zip-full p7zip-rar fonts-dejavu \
htop xclip meld curl \
wget extra-cmake-modules \
mesa-common-dev libglu1-mesa-dev vlc flatpak gimp zsh gettext \
libtool libtool-bin autoconf automake pkg-config unzip fonts-hack-ttf

# Gnome packages / Tweaks
gsettings set org.gnome.shell.extensions.dash-to-dock click-action 'minimize'
sudo apt install gnome-tweaks gnome-shell-extensions

# Fsearch installation
sudo add-apt-repository ppa:christian-boxdoerfer/fsearch-stable
sudo apt update
sudo apt install fsearch

# To remove apt key deprecated warning due to above commands follow the instruction here: 
# https://askubuntu.com/questions/1398344/apt-key-deprecation-warning-when-updating-system

# Snap refresh
sudo snap refresh

# Configure flathub
flatpak remote-add --if-not-exists flathub https://flathub.org/repo/flathub.flatpakrepo

echo "Configure git username/email"
git config --global user.name "Sonu Lohani"
git config --global user.email "sonulohani@gmail.com"
git config --global merge.tool meld
git config --global diff.tool meld
ssh-keygen -t rsa -b 4096 -C "sonulohani@gmail.com"
eval "$(ssh-agent -s)"
ssh-add ${HOME}/.ssh/id_rsa
xclip -sel clip < ~/.ssh/id_rsa.pub

# tmux
cd
git clone https://github.com/gpakosz/.tmux.git
ln -s -f .tmux/.tmux.conf
cp .tmux/.tmux.conf.local .
# For more info: https://www.youtube.com/watch?v=cPWEX2446B4

echo "Installing Spacevim"
curl -sLf https://spacevim.org/install.sh | bash

echo "Enabling firewall"
sudo systemctl enable ufw

echo "Install ohmyzsh"
cd ${HOME}
sh -c "$(curl -fsSL https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)"

echo "Installing zsh-autosuggestions"
git clone https://github.com/zsh-users/zsh-autosuggestions ${ZSH_CUSTOM:-~/.oh-my-zsh/custom}/plugins/zsh-autosuggestions

echo "Installing zsh-syntax-highlighting"
git clone https://github.com/zsh-users/zsh-syntax-highlighting.git ${ZSH_CUSTOM:-~/.oh-my-zsh/custom}/plugins/zsh-syntax-highlighting

sed -i 's/ZSH_THEME="robbyrussell"/ZSH_THEME="random"/g' ~/.zshrc
sed -i 's/plugins=(git)/plugins=(git zsh-autosuggestions zsh-syntax-highlighting)/g' ~/.zshrc
sed -i -e '$a\export PATH="/home/linuxbrew/.linuxbrew/bin:/home/linuxbrew/.linuxbrew/sbin:~/.local/bin:$PATH"' ~/.zshrc
sed -i -e '$a\eval "$(starship init zsh)"' ~/.zshrc

# Install homebrew
# https://brew.sh/
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Homebrew packages
brew install neovim gcc gdb git neofetch the_silver_searcher cmake extra-cmake-modules ninja nano curl tmux starship aria2 ffmpeg

######################################## Optional setup ########################################

echo "Installing powerlevel10k"
git clone --depth=1 https://github.com/romkatv/powerlevel10k.git ${ZSH_CUSTOM:-$HOME/.oh-my-zsh/custom}/themes/powerlevel10k


# ZSH Manually setup----------------------------------------------------
# ZSH_THEME="powerlevel10k/powerlevel10k"
# plugins=(git zsh-autosuggestions zsh-syntax-highlighting)
# My changes begin                                                              
# export PATH=${HOME}/Programs:$PATH                                          
# My changes end  
#------------------------------------------------------------------------

# echo "Installing optional packages"
# sudo apt install -y ubuntu-restricted-extras dconf-editor timeshift terminator snapd qt5-default obs-studio 

# Clang
https://apt.llvm.org/

# Fonts
https://github.com/tonsky/FiraCode
https://github.com/adobe-fonts/source-code-pro
https://github.com/microsoft/cascadia-code
https://www.nerdfonts.com/font-downloads
https://github.com/i-tu/Hasklig
https://github.com/madmalik/mononoki
https://typeof.net/Iosevka/
https://input.djr.com/download/?customize&fontSelection=whole&a=ss&g=ss&i=serifs&l=serifs&zero=slash&asterisk=height&braces=0&preset=monaco&line-height=1.4&email=

# Nerd fonts
# Cascadia code
# Code New Roman

# deb-get
curl -sL https://raw.githubusercontent.com/wimpysworld/deb-get/main/deb-get | sudo -E bash -s install deb-get
deb-get install google-chrome-stable code fsearch

# Extra
# Install chrome
# Install code
# Install virtualbox
# Install PlugInstall
# Install k2pdfopt, openshot, mypaint, inkscape
# change font in terminator and gnome-terminal
# Extensions: Clipboard indicator, https://extensions.gnome.org/extension/3193/blur-my-shell/, Desktop Icons NG(DING), KStatusNotifierItem/AppIndicator Support
# https://extensions.gnome.org/extension/4937/draw-on-you-screen-2/, https://extensions.gnome.org/extension/1238/time/, Night theme switcher, Removable driver menu, https://extensions.gnome.org/extension/1262/bing-wallpaper-changer/, https://extensions.gnome.org/extension/4269/alphabetical-app-grid/
# xclip -sel clip < ~/.ssh/id_rsa.pub
# https://github.com/source-foundry/font-line
# https://nomacs.org/download/

# peek
# https://github.com/phw/peek

# For terminal themes
# bash -c  "$(wget -qO- https://git.io/vQgMr)"

# Install Joplin
# https://joplinapp.org/

echo "Removing unnecessary packages"
# sudo apt purge -y thunderbird gnome-mahjongg gnome-mines gnome-sudoku aisleriot
# sudo apt autoremove --purge -y
