FROM docker.io/library/ubuntu:rolling

RUN apt-get update && \
    apt-get install -y \
    nala

RUN nala install -y build-essential g++ gdb libglfw3-dev cmake extra-cmake-modules \
    libglew-dev libsoil-dev libglm-dev python3-pip build-essential binutils cmake-qt-gui \
    g++ gdb git rar unrar p7zip-full p7zip-rar fonts-dejavu \
    htop xclip meld curl wget extra-cmake-modules \
    mesa-common-dev libglu1-mesa-dev gettext ninja-build \
    libtool libtool-bin autoconf automake pkg-config unzip fonts-hack-ttf \
    silversearcher-ag aria2 zsh \
    ripgrep fd-find software-properties-common

RUN add-apt-repository ppa:zhangsongcui3371/fastfetch && apt-get update && apt install fastfetch -y

RUN nala update && nala install -y sudo

# Set password variable
ARG PASSWORD=docker

# Generate password hash
RUN apt-get update && apt-get install -y --no-install-recommends \
    openssl \
  && rm -rf /var/lib/apt/lists/* \
  && usermod --lock root \
  && echo "ubuntu:$PASSWORD" | chpasswd \
  && usermod --unlock root

# Set default user
USER ubuntu
