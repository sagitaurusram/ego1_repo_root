VisualSVN Server
 Code-Box / Projects Codes / Radar_BF70x / DemoRad_R-1-2-2 / R-1-2-2 / Software / Python / AN24-00 / demorad-setup.shRevision: HEAD   
Raw
#!/bin/bash

SUDO="sudo"
APT="apt"
PIP="pip3"
UDEV="udevadm"

APT_PACKAGES="python3 python3-pip python3-pyqtgraph python3-numpy libusb-1.0.0 usbutils"
PIP_PACKAGES="pyusb"

UDEV_PATH="/lib/udev/rules.d/90-demorad.rules"

# This is the setup script to run the DemoRad board on Linux


# Update the package repository
$SUDO $APT update

# Install necessary packages
$SUDO $APT --assume-yes install $APT_PACKAGES

# Install pyusb via pip
$SUDO $PIP install $PIP_PACKAGES

# Create a udev rule for the DemoRad board
$SUDO echo 'ACTION=="add", SUBSYSTEMS=="usb", ATTRS{idVendor}=="064b", ATTRS{idProduct}=="7823", MODE="660", GROUP="plugdev"' > $UDEV_PATH

# Restart udev
$SUDO $UDEV control --reload && $SUDO $UDEV trigger

echo "The system is now set up for the DemoRad board."