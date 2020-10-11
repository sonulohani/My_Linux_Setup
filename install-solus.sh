#!/usr/bin/env bash

set -eu;

SCRIPT_DIR=$(pwd);

cd ${HOME};

echo "Removing unnecessary packages";
sudo eopkg remove -y thunderbird firefox gnome-mpv;

echo "Updating the system";
sudo eopkg up;

echo "Installing essential packages";
sudo eopkg install -y binutils vlc gufw git gcc make vscode gdb neofetch gnome-font-viewer cmake \
extra-cmake-modules meld xclip zsh obs-studio uget htop gimp llvm-clang lldb silver-searcher \
virtualbox-current micro neovim;

sudo eopkg install -y -c system.devel;

echo "Installing Linux headers";
sudo eopkg install -y linux-current-headers;

echo "Installing MS Fonts";
sudo eopkg bi --ignore-safety https://raw.githubusercontent.com/getsolus/3rd-party/master/desktop/font/mscorefonts/pspec.xml;
sudo eopkg it mscorefonts*.eopkg;sudo rm mscorefonts*.eopkg;

echo "Installing Google chrome";
sudo eopkg bi --ignore-safety https://raw.githubusercontent.com/getsolus/3rd-party/master/network/web/browser/google-chrome-stable/pspec.xml;
sudo eopkg it google-chrome-*.eopkg;sudo rm google-chrome-*.eopkg;

echo "Cleaning eopkg";
sudo eopkg rmo;

echo "Upgrading pip3";
pip3 install --user --upgrade pip;

echo "Installing VimPlug and configure neovim";
pip3 install --user neovim;
sh -c 'curl -fLo "${XDG_DATA_HOME:-$HOME/.local/share}"/nvim/site/autoload/plug.vim --create-dirs \
       https://raw.githubusercontent.com/junegunn/vim-plug/master/plug.vim';
mkdir -p ${HOME}/.config/nvim;
cp ${SCRIPT_DIR}/init.vim ${HOME}/.config/nvim;

echo "Configure git username/email";
git config --global user.name "Sonu Lohani";
git config --global user.email "sonulohani@gmail.com";

echo "Copying fonts";
mkdir -p ${HOME}/.local/share/fonts;
cp -r ${SCRIPT_DIR}/fonts/* ${HOME}/.local/share/fonts;
fc-cache -fv;

echo "Enabling firewall";
sudo systemctl enable ufw;

echo "Setting ssh";
ssh-keygen -t rsa -b 4096 -C "sonulohani@gmail.com";
eval "$(ssh-agent -s)";
ssh-add ${HOME}/.ssh/id_rsa;

echo "Install ohmyzsh";
cd ${HOME};
sh -c "$(curl -fsSL https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)";

# Extra
# Install chrome
# Install code
# Install virtualbox
# Install PlugInstall
# Install k2pdfopt, openshot, mypaint, inkscape
# change font in terminator and gnome-terminal
# Extensions: Caffeine, clipboard indicator, dash to dock(enable trash and click to minimize), blyr, TopIcon Plus, Desktop Icons NG(DING), KStatusNotifierItem/AppIndicator Support
# Pop Shell, Night theme switcher, Removable driver menu, 
# xclip -sel clip < ~/.ssh/id_rsa.pub

# For terminal themes
# bash -c  "$(wget -qO- https://git.io/vQgMr)"

# Add pip3 Path in .zshrc
# My changes begin
# export PATH=${HOME}/.local/bin:${PATH}
# My changes end

