# KNX to MQTT to Lecnet 
This project is created for personal use in a home automation setup. The setup is based on a LogicMachine KNX device, NodeRed, RaspberryPi and Lectrosonics DM1624 (LecNet).

The data flow is pretty simple:
1) LogicMachine publishes changes on KNX bus (KNX IP)
2) NodeRed listens to KNX IP
3) NodeRed transforms KNX input into custom messages
4) NodeRed publishes these messages to MQTT
5) Raspberry Pi (Python script) listens to MQTT
6) Raspberry Pi transforms custom messages from MQTT into LecNet serial commands
7) Raspberry Pi connects and sends these messages via USB to the DM1624

The Lectrosonics DM1624 has both serial and USB, but on my device I could not get the serial device working. The only interface left was the USB, which turns out to be a FTDI device with a custom VID(1321)/PID(1001) and baud of 57600. By setting this in a Python script on connect, it connects just fine. The device I use can be found here: https://www.lectrosonics.com/Support/LecNet2-Series/lecnet2.html

## Prerequisites
* Python 3.x
* libftdi

By running the `setup.sh` as root on the Raspberry Pi you are going to run, you install the requires libraries and packages.
This script also injects a line to allow your script to connect to the USB device later:
```
echo SUBSYSTEMS=="usb", ATTRS{idVendor}=="1321", ATTRS{idProduct}=="1001", GROUP="dialout", MODE="0660" >> /etc/udev/rules.d/99-libftdi.rules
```

## Usage
Copy `config.sample.py` to `config.py` and edit to fit your config. Run the `setup.sh` as a elevate user. Run `python manual.py` to test. Run `python mqtt.py` to run full project.

The `node-red-config.json` can be added to your NodeRed instance to use my config exactly as is. Recommended to update the IP settings, and execute the "Init default state" injection to generate a default state file. 

## Known issues
### EQ 
The DM1624 has a pretty bad EQ out of the box. I ran a calibration of the input to try to achieve a flat frequency response.  This is recommended, and if wanted, I could add the EQ settings used to get as flat response as wanted.
### Input clipping
I experienced some peak/clipping when listening to music in my initial testing, which led me to add the lines in `mqtt.py` that sets the input gain levels to -5.