# Python Station Scan (Scapy)

With Python, you can also evaluate probe requests. All you need is the Scapy library, and some Python code. I developed this Python script for my own station analysis. If you like it, you can freely use it and further develop it. In addition, there is also a small [bash script](../BashMonitorMode) which helps you to set the monitor mode for the respective interface.

## Objective

The aim of this tutorial is to analyse Wi-Fi stations with Python Scapy.

## Install needed and/or optional packages

Install (_or ensure they are installed_) following packages.

```shell
# update system (optional)
$ sudo apt update -y && sudo apt upgrade -y

# install needed packages
$ sudo apt install -y python3-pip curl

# install scapy (latest)
$ sudo pip3 install scapy
```

## Download and prepare all scripts

```shell
# change into home directory
$ cd ~

# download bash script
$ curl -L https://raw.githubusercontent.com/Lupin3000/Raspberry-PI-Tutorials/main/Goodies/BashMonitorMode/monitor-mode.sh -o monitor-mode.sh

# download python script
$ curl -L https://raw.githubusercontent.com/Lupin3000/Raspberry-PI-Tutorials/main/Goodies/PythonStationScan/StationScan.py -o StationScan.py

# set file permissions
$ chmod u+x monitor-mode.sh
$ chmod u+x StationScan.py
```

## Enable Monitor Mode

```shell
# show help (optional)
$ ./monitor-mode.sh -h

# enable monitor mode
$ sudo ./monitor-mode -i wlan1
```

## Scan for stations

```shell
# show help (optional)
$ ./StationScan.py --help

# scan stations (incl. hidden SSID)
$ sudo ./StationScan.py wlan1

# scan stations (excl. hidden SSID)
$ sudo ./StationScan.py wlan1 --filter
```

[Go Back](../../readme.md)