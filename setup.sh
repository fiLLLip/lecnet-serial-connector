apt-get install libftdi-dev -y
apt-get install python3-pip -y
pip3 install paho-mqtt pylibftdi
echo SUBSYSTEMS=="usb", ATTRS{idVendor}=="1321", ATTRS{idProduct}=="1001", GROUP="dialout", MODE="0660" >> /etc/udev/rules.d/99-libftdi.rules