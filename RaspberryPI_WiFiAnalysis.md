# Analyze Wi-Fi with Raspberry PI

Even without a GUI (_no Desktop_) you can very quickly analyze your Wi-Fi environment with the Raspberry PI. For this you can use tools like [Aircrack-ng](https://www.aircrack-ng.org/) or other well-known Linux tools.

## Objective

Wi-Fi analysis without Aircrack-ng in a few steps with tcpdump and wavemon.

## Install needed and/or optional packages

Install (_or ensure they are installed_) following packages.

```shell
# update system (optional)
$ sudo apt update -y && sudo apt upgrade -y

# install optional packages (optional)
$ sudo apt install -y vim wireless-tools

# install needed packages
$ sudo apt install -y tcpdump wavemon
```

## Preparation

If you have already set up an AP and/or a Captive portal, you should stop them now.

```shell
# stop nodogsplash service
$ sudo systemctl stop nodogsplash

# stop hostapd service
$ sudo systemctl stop hostapd

# stop dnsmasq service
$ sudo systemctl stop dnsmasq
```

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

## tcpdump

### Analyze STA's

To analyze STA's you capture `probe-req` with tcpdump.

```shell
# capture STA's looking for SSID
$ sudo tcpdump -i wlan1 -s 0 type mgt subtype probe-req

# capture STA's looking for SSID and show mac address
$ sudo tcpdump -i wlan1 -s 0 -e type mgt subtype probe-req
```

That's looking ugly, do you know `grep`?

```shell
# filter SSID's with grep
$ sudo tcpdump -i wlan1 -s 0 -l type mgt subtype probe-req | grep -o -P '\(\K[^\)]+'

# filter mac addresses with grep
$ sudo tcpdump -i wlan1 -s 0 -l -e type mgt subtype probe-req | grep -o -E '([[:xdigit:]]{2}:){5}[[:xdigit:]]{2}'
```

Nobody like to watch all the time on the screen, you can save all informations to a text file.

```shell
# save to file
$ sudo tcpdump -i wlan1 -s 0 -l type mgt subtype probe-req | grep -o -P '\(\K[^\)]+' --line-buffered | tee -a STAs.txt

# sort duplicates and count them
$ sort STAs.txt | uniq -cd
```

### Analyze AP's

To analyze AP's you capture `beacon` and/or `probe-resp`.

```shell
# capture AP's
$ sudo tcpdump -i wlan1 -e -s 256 -l type mgt subtype beacon or subtype probe-resp
```

### Channel hopping

In order not to always have to change the channel manually, create a bash script (_channel_hopping.sh_) that does the work for you in the background.

```shell
# create bash script
$ vim channel_hopping.sh

# change permissions
$ chmod u+x channel_hopping.sh

# run in backgroud
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

Wavemon is another awesome Wi-Fi analyzing tool, which is very simple to us. But set back you interface into "managed mode" first!

```shell
# set interface down
$ sudo ip link set wlan1 down

# turn interface into managed mode
$ sudo iwconfig wlan1 mode managed

# set interface up
$ sudo ip link set wlan1 up

# start wavemon
$ sudo wavemon -i wlan1
```

Press `F3` key to scan and later later `F10` key to exit.

[Go Back](./README.md)
