# Analyze Wi-Fi with Raspberry PI

Even without a GUI (_no Desktop_) you can very quickly analyze the Wi-Fi environment around you.

## Objective

The aim of this tutorial is to analyze stations and access points in order to better lure people and devices into the honey pot.

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
$ sudo apt install -y vim wireless-tools

# install needed packages
$ sudo apt install -y tcpdump wavemon aircrack-ng
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

# set interface to specific channel
$ sudo iwconfig wlan1 channel 9
```

_Note: Read this [Wikipedia article](https://en.wikipedia.org/wiki/Monitor_mode) to get more information._

## tcpdump

### Analyze STA's

To analyze STA's, which do looking for already know access points, you can capture there `probe-req` with tcpdump.

```shell
# capture STA's looking for SSID
$ sudo tcpdump -i wlan1 -s 0 type mgt subtype probe-req

# capture STA's looking for SSID and show mac address
$ sudo tcpdump -i wlan1 -s 0 -e type mgt subtype probe-req
```

That output is looking ugly, do you know `grep`?

```shell
# filter SSID's with grep
$ sudo tcpdump -i wlan1 -s 0 -l type mgt subtype probe-req | grep -o -P '\(\K[^\)]+'

# filter mac addresses with grep
$ sudo tcpdump -i wlan1 -s 0 -l -e type mgt subtype probe-req | grep -o -E '([[:xdigit:]]{2}:){5}[[:xdigit:]]{2}'
```

Nobody like to watch all the time on the screen, you can save all information's to a text file.

```shell
# save to file
$ sudo tcpdump -i wlan1 -s 0 -l type mgt subtype probe-req | grep -o -P '\(\K[^\)]+' --line-buffered | tee -a STAs.txt

# sort duplicates and count them
$ sort STAs.txt | uniq -cd
```

### Analyze AP's

To analyze access points around you, you can capture `beacon` and/or `probe-resp` with tcpdump.

```shell
# capture AP's
$ sudo tcpdump -i wlan1 -e -s 256 -l type mgt subtype beacon or subtype probe-resp
```

### Channel hopping

In order not to always have to change the channel manually, create a tiny bash script (_channel_hopping.sh_) that does the work for you in the background.

```shell
# create bash script
$ vim channel_hopping.sh

# change permissions
$ chmod u+x channel_hopping.sh

# run in background
$ sudo ./channel_hopping.sh &
```

The content of `channel_hopping.sh`.

```shell
#!/usr/bin/env bash

echo "Current PID: $$"

while true; do
  for channel in {1..14}; do
    echo "Current Channel: $channel"
    iwconfig wlan1 channel $channel
    sleep 2
  done
done
```

## Wavemon

Wavemon is another awesome Wi-Fi analyzing tool, which is very simple to us.

_Note: Please set back you interface into "managed mode" first!_

```shell
# set interface down
$ sudo ip link set wlan1 down

# turn interface into managed mode
$ sudo iwconfig wlan1 mode managed

# set interface up
$ sudo ip link set wlan1 up
```

Execute Wavemon

```shell
# show help (optional)
$ wavemon -h

# start wavemon
$ sudo wavemon -i wlan1
```

Press `F3` key to scan, `F2` to show the histogram, press `F10` key to exit.

_Note: Read this [man page](http://manpages.ubuntu.com/manpages/bionic/man1/wavemon.1.html) to learn more about Wavemon._

## airodump-ng (Aircrack-ng)

The Aircrack-ng suite includes many tools to assess Wi-Fi networks. Here the focus is on `airodump-ng` only. Please set your interface `wlan1` into monitor mode first (_but no need to specify the channel_)!

```shell
# show help (optional)
$ airodump-ng --help

# run the simplest airodump
$ sudo airodump-ng -i wlan1

# run more precise airodump
$ sudo airodump-ng -i wlan1 --manufacturer --wps --ignore-negative-one
```

Press `CTRL` + `c` keys to stop the scan and exit.

_Note: Read the [online documentation](https://www.aircrack-ng.org/) to get more information._

[Go Back](../readme.md)
