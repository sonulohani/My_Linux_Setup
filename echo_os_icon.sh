#!/bin/bash

# Define icons for different distros
UBUNTU_ICON=""
MINT_ICON="󰣭"
DEBIAN_ICON=""
FEDORA_ICON=""
ARCH_ICON="󰣇"
UNKNOWN_ICON="❓"

# Read the distro information from /etc/os-release
if [ -f /etc/os-release ]; then
	. /etc/os-release
else
	echo "$UNKNOWN_ICON"
	exit 1
fi

# Check the ID or NAME variables to determine the distro and echo the corresponding icon
case "$ID" in
ubuntu)
	echo "$UBUNTU_ICON"
	;;
linuxmint)
	echo "$MINT_ICON"
	;;
debian)
	echo "$DEBIAN_ICON"
	;;
fedora)
	echo "$FEDORA_ICON"
	;;
arch)
	echo "$ARCH_ICON"
	;;
*)
	echo "$UNKNOWN_ICON"
	;;
esac
