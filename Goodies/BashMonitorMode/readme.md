# Python Access Point Scan (Scapy)

With Python, you can also evaluate beacons and  probe responses. All you need is the Scapy library, and some Python code. I developed this Python script for my own access point analysis. If you like it, you can freely use it and further develop it. In addition, there is also a small [bash script](../BashMonitorMode) which helps you to set the monitor mode for the respective interface.

## Objective

The aim of this tutorial is to analyse Wi-Fi access points with Python Scapy.

## Install needed and/or optional packages

Install (_or ensure they are installed_) following packages.

```shell
# update system (optional)
$ sudo apt update -y && sudo apt upgrade -y

# install optional packages (optional)
$ sudo apt install -y wireless-tools

# install needed packages
$ sudo apt install -y curl
```

## Download and prepare Bash script

```shell
# change into home directory
$ cd ~

# download bash script
$ curl -L https://raw.githubusercontent.com/Lupin3000/Raspberry-PI-Tutorials/main/Goodies/BashMonitorMode/monitor-mode.sh -o monitor-mode.sh

# set file permissions
$ chmod u+x monitor-mode.sh
```

## Enable Monitor Mode

```shell
# show help (optional)
$ ./monitor-mode.sh -h

# enable monitor mode
$ sudo ./monitor-mode -i wlan1
```

[Go Back](../../readme.md)
