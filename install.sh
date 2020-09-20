#!/usr/bin/env bash

set -eu

SCRIPT_DIR=$(pwd)

cd ${HOME}

echo "Removing unnecessary packages"
sudo apt purge -y thunderbird gnome-mahjongg gnome-mines gnome-sudoku aisleriot
sudo apt autoremove --purge -y

echo "Updating the system"
sudo apt update && sudo apt upgrade -y

echo "Installing essential packages"
sudo apt install -y python3-pip build-essential binutils neovim cmake-qt-gui \
timeshift gufw g++ gdb git terminator ubuntu-restricted-extras rar unrar p7zip-full \
p7zip-rar neofetch htop silversearcher-ag xclip meld obs-studio snapd flatpak \
clang-format clang-tidy clang-tools clang clangd libc++-dev libc++1 libc++abi-dev \
libc++abi1 libclang-dev libclang1 liblldb-dev libllvm-ocaml-dev libomp-dev libomp5 \
lld lldb llvm-dev llvm-runtime llvm python-clang apt-transport-https zsh curl gimp \
gnome-tweaks gnome-shell-extensions uget wget network-manager-openvpn-gnome

echo "Enabling trash icon in dock"
gsettings set org.gnome.nautilus.desktop trash-icon-visible true

echo "Creating Programs folder"
mkdir -p ${HOME}/Programs
cd ${HOME}/Programs && curl https://getmic.ro | bash && cd -

echo "Configure git username/email"
git config --global user.name "Sonu Lohani"
git config --global user.email "sonulohani@gmail.com"

echo "Installing VimPlug and configure neovim"
sh -c 'curl -fLo "${XDG_DATA_HOME:-$HOME/.local/share}"/nvim/site/autoload/plug.vim --create-dirs \
       https://raw.githubusercontent.com/junegunn/vim-plug/master/plug.vim'
mkdir -p ${HOME}/.config/nvim
cp ${SCRIPT_DIR}/init.vim ${HOME}/.config/nvim

echo "Copying fonts"
mkdir -p ${HOME}/.local/share/fonts
cp -r ${SCRIPT_DIR}/fonts/* ${HOME}/.local/share/fonts
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/JetBrains/JetBrainsMono/master/install_manual.sh)"
fc-cache -fv

echo "Enabling firewall"
sudo systemctl enable ufw

echo "Installing terminator theme plugin"
pip3 install requests
mkdir -p $HOME/.config/terminator/plugins
wget https://git.io/v5Zww -O $HOME"/.config/terminator/plugins/terminator-themes.py"

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

# Extra
# ZSH Manually setup----------------------------------------------------
# ZSH_THEME="powerlevel10k/powerlevel10k"
# plugins=(git zsh-autosuggestions zsh-syntax-highlighting)
# My changes begin                                                              
# export PATH=${HOME}/Programs:$PATH                                          
# My changes end  
#------------------------------------------------------------------------
# Install chrome
# Install code
# Install virtualbox
# Install PlugInstall
# Install k2pdfopt, openshot, mypaint, inkscape
# change font in terminator and gnome-terminal
# Extensions: Caffine, clipboard indicator, dash to dock


