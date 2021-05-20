# WI-FI Monitor Mode with Raspberry PI Zero

The Raspberry Pi models have a Broadcom BCM43438 wireless chipset (_2.4GHz_). Out of the box (_Standard Raspbian OS_) it is not possible to enable the Wi-Fi Monitor Mode, even if the chip would support it.

## Objective

The aim of this tutorial is to show how you can patch the kernel to make the Monitor Mode possible.

## Precondition

You should already have read (_and successful carried out_) the following tutorials.

- [Setup Raspberry PI](../Setup)
- [Prepare Raspberry PI](../Preparation)

## Install needed and/or optional packages

Install (_or ensure they are installed_) following packages.

```shell
# update system (optional)
$ sudo apt update -y && sudo apt upgrade -y

# install optional packages (optional)
$ sudo apt install -y wireless-tools build-essential curl
```

## Re4son-Kernel for Raspberry Pi

### Installation

The simplest way is to use the Re4son-Pi-Kernel, [here](https://re4son-kernel.com/re4son-pi-kernel/) you will find all information about.

```shell
# download latest archive
$ curl -L -C - https://re4son-kernel.com/download/re4son-kernel-current/ -o re4son-kernel_current.tar.xz

# unzip archive
tar -xJf re4son-kernel_current.tar.xz

# change into extracted folder
cd re4son-kernel_*

# run installation
sudo ./install.sh
```

_Note: Be patient, the process will take some time. You can also answer all questions with "Y" (yes)._

### Prepare interface

After the successful installation and reboot, you need to create a new interface (_already in Monitor Mode_).

```shell
# create new wireless devices incl. configuration
$ sudo iw phy phy0 interface add mon0 type monitor

# start created interface
$ sudo ifconfig mon0 up

# verify interfaces (optional)
$ iw phy phy0 info
```

_Note: Just create a small bash script, and a service to automate this process._

### Scan for AP's and STA's

From now on you can use all known tools, or the Python scripts I have created.

```shell
# install needed packages
$ sudo apt install -y python3-pip curl

# install scapy
$ sudo pip3 install scapy

# download Python STA scanner
$ curl -L https://raw.githubusercontent.com/Lupin3000/Raspberry-PI-Tutorials/main/Goodies/PythonStationScan/StationScan.py -o StationScan.py

# set permissions
$ chmod +x StationScan.py

# run STA scanner
$ sudo ./StationScan.py mon0

# download Python AP scanner
$ curl -L https://raw.githubusercontent.com/Lupin3000/Raspberry-PI-Tutorials/main/Goodies/PythonAccessPointScan/AccessPointScan.py -o AccessPointScan.py

# set permissions
$ chmod +x AccessPointScan.py

# run AP scanner
$ sudo ./AccessPointScan.py mon0 --all
```

[Go Back](../readme.md)
