### Install nala
https://gitlab.com/volian/nala/-/releases

### Updating the system
```
sudo nala update && sudo nala upgrade
```

### Installing essential packages
```
sudo nala install -y python3-pip build-essential binutils cmake-qt-gui \
g++ gdb git rar unrar p7zip-full p7zip-rar fonts-dejavu \
htop xclip meld curl wget extra-cmake-modules \
mesa-common-dev libglu1-mesa-dev vlc flatpak gimp gettext ninja-build \
libtool libtool-bin autoconf automake pkg-config unzip fonts-hack-ttf \
neofetch silversearcher-ag aria2 ffmpeg nomacs mpv \
clang-format clang-tidy clang-tools clang clangd libc++-dev libc++1 \
libc++abi-dev libc++abi1 libclang-dev libclang1 liblldb-dev libllvm-ocaml-dev libomp-dev \
libomp5 lld lldb llvm-dev llvm-runtime llvm python3-clang zsh uidmap python3-virtualenv
```

### Neovim
```
sudo add-apt-repository ppa:neovim-ppa/unstable
sudo nala update && sudo nala install neovim
git clone --depth 1 https://github.com/AstroNvim/AstroNvim ~/.config/nvim
```

### Gnome packages / Tweaks
```
gsettings set org.gnome.mutter center-new-windows true
gsettings set org.gnome.shell.extensions.dash-to-dock click-action 'minimize'
gsettings set org.gnome.nautilus.preferences open-folder-on-dnd-hover true
sudo nala install gnome-tweaks gnome-shell-extensions
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
ssh-keygen -t rsa -b 4096 -C "sonulohani@gmail.com"
eval "$(ssh-agent -s)"
ssh-add ${HOME}/.ssh/id_rsa
xclip -sel clip < ~/.ssh/id_rsa.pub
```

### Vim plug
```
sh -c 'curl -fLo "${XDG_DATA_HOME:-$HOME/.local/share}"/nvim/site/autoload/plug.vim --create-dirs \
       https://raw.githubusercontent.com/junegunn/vim-plug/master/plug.vim'
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
sed -i 's/ZSH_THEME="robbyrussell"/ZSH_THEME="random"/g' ~/.zshrc
sed -i 's/plugins=(git)/plugins=(git zsh-autosuggestions zsh-syntax-highlighting emoji emotty)/g' ~/.zshrc
```

### Neovim init.vim
```
mkdir -p ~/.config/nvim && cat <<EOF >~/.config/nvim/init.vim
call plug#begin()

Plug 'https://github.com/vim-airline/vim-airline' " Status bar
Plug 'https://github.com/preservim/nerdtree' " NerdTree
Plug 'preservim/nerdcommenter'

call plug#end()

filetype plugin indent on
set number
set relativenumber
set mouse=a
set tabstop=4 softtabstop=4 shiftwidth=4 expandtab smarttab autoindent
set incsearch ignorecase smartcase hlsearch
set wildmode=longest,list,full wildmenu
set ruler laststatus=2 showcmd showmode
set list listchars=trail:»,tab:»-
set fillchars+=vert:\ 
set wrap breakindent
set encoding=utf-8
set textwidth=0
set hidden
set title
set clipboard+=unnamedplus

nnoremap <C-f> :NERDTreeFocus<CR>
nnoremap <C-n> :NERDTree<CR>
nnoremap <C-t> :NERDTreeToggle<CR>

let mapleader=","
let g:NERDTreeDirArrowExpandable="+"
let g:NERDTreeDirArrowCollapsible="~"
EOF
```

### Install opensnitch
[Opensnitch](https://github.com/evilsocket/opensnitch)

### Brew

#### Installing brew
```
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

#### Adding brew to .zprofile and .zshrc
```
(echo; echo 'eval "$(/home/linuxbrew/.linuxbrew/bin/brew shellenv)"') >> /home/sonul/.zprofile
eval "$(/home/linuxbrew/.linuxbrew/bin/brew shellenv)"
sed -i -e '$a\export PATH="/home/linuxbrew/.linuxbrew/bin:/home/linuxbrew/.linuxbrew/sbin:/home/sonul/.local/bin:$PATH"' ~/.zshrc
```

#### Brew install packages
```
brew install podman gcc gdb neovim
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

### Tlp
```
sudo apt install tlp tlp-rdw
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
### Qt alternative tool
 - Doc link - https://aqtinstall.readthedocs.io/_/downloads/en/latest/pdf/
 - Tool link - https://github.com/engnr/qt-downloader
```
aqt install-qt linux desktop 6.4.3 gcc_64 -O /home/sonul/Qt
aqt install-tool linux desktop tools_qtcreator_gui -O /home/sonul/Qt
aqt install-example linux desktop 6.4.3 -O /home/sonul/Qt/6.4.3/
```
