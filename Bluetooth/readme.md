# Bluetooth Basics and Analysis with Raspberry PI

The Raspberry PI already comes with a Bluetooth device. This is very good because you can achieve a lot with it. Since many Bluetooth device manufacturers want to make the connection as easy as possible for users, you can start with the analysis.

## Objective

The aim of this tutorial is to learn some Bluetooth basics and to start with the Bluetooth analysis.

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
$ sudo apt install -y bluez bluez-hcidump
```

## Some basics first

With bluez you have already some common tools available on Raspberry PI - for example `hcitool`, `bluetoothctl`, `sdptool` and `gattool`.

### Controller

Some basic commands for the controller with `bluetoothctl`.

```shell
# verify Bluetooth service is enabled (optional)
$ sudo systemctl status bluetooth.service

# access Bluetooth control
$ sudo bluetoothctl

# show help (optional)
[bluetooth]# help

# enable controller auto-power (optional)
[bluetooth]# power on

# list available controllers
[bluetooth]# list

# show all controller information's
[bluetooth]# show

# show specific controller information
[bluetooth]# show [mac address]

# select default controller (optional)
[bluetooth]# select [mac address or alias]

# show environment variables (optional)
[bluetooth]# export

# exit bluetoothctl (same as quit command)
[bluetooth]# exit
```

Now with the `hcitool`.

```shell
# show help (optional)
$ hcitool --help

# display local devices
$ sudo hcitool dev
```

**Scan for devices**

Now already the cool stuff, you start to analyze what devices are around with `bluetoothctl`.

```shell
# enable agent
[bluetooth]# agent on

# set agent as the default one
[bluetooth]# default-agent

# start scan for devices
[bluetooth]# scan on

# stop scan for devices
[bluetooth]# scan off
```

- [NEW] means 'found new devices'
- [CHG] means 'device has changed'
- [DEL] means 'device deleted'

Scan with the `hcitool`.

```shell
# scan for remote devices
$ sudo hcitool scan

# scan for remote devices (incl. information and oui)
$ sudo hcitool scan --info --oui

# start passive LE scan (default is active)
$ sudo hcitool lescan --passive

# start active LE scan (don't filter duplicates)
$ sudo hcitool lescan --duplicates
```

### Analysis of Devices

While the scan is running (_or quickly after the stop_), you can try to get more information about the devices. You have to be fast!

```shell
# start scan for devices
[bluetooth]# scan on
...
[NEW] Device E8:38:80:7F:E3:D7 root
...

# show device information
[bluetooth]# info E8:38:80:7F:E3:D7
Device E8:38:80:7F:E3:D7 (public)
	Name: root
	Alias: root
	Class: 0x007a020c
	Icon: phone
	Paired: no
	Trusted: no
	Blocked: no
	Connected: no
	...

# stop scan for devices
[bluetooth]# scan off
```

Again with the `hcitool`.

```shell
# show specific device information
$ sudo hcitool info E8:38:80:7F:E3:D7
Requesting information ...
	BD Address:  E8:38:80:7F:E3:D7
	OUI Company: Apple, Inc. (E8-38-80)
	Device Name: root
	...

# show specific LE device information
$ sudo hcitool leinfo 4D:87:7A:55:2F:31
Requesting information ...
	Handle: 64 (0x0040)
	LMP Version: 4.2 (0x8) LMP Subversion: 0x35f4
	Manufacturer: Cambridge Silicon Radio (10)
```

Wow ... the showed information's are really great. With this information you know already a lot about the device! Store this information and continue with your Bluetooth analysis.

After the scan is stopped, all devices will be deleted soon.

```shell
...
[DEL] Device E8:38:80:7F:E3:D7 root
...
[bluetooth]# info E8:38:80:7F:E3:D7
Device E8:38:80:7F:E3:D7 not available
```

Dive deeper with `sdptool`.

```shell
# show help (optional)
$ sdptool --help

# show all available services
$ sudo sdptool browser E8:38:80:7F:E3:D7
...
Service Name: Phonebook
Service RecHandle: 0x4f49112f
Service Class ID List:
  "Phonebook Access - PSE" (0x112f)
Protocol Descriptor List:
  "L2CAP" (0x0100)
  "RFCOMM" (0x0003)
    Channel: 13
  "OBEX" (0x0008)
...
```

You will see (_with sdptool_) much more information! For example services, channel and protocols. The following services can be discovered.

DID SP DUN LAN FAX OPUSH FTP PRINT HS HSAG HF HFAG SAP PBAP MAP NAP GN PANU HCRP HID KEYB WIIMOTE CIP CTP A2SRC A2SNK AVRCT AVRTG UDIUE UDITE SEMCHLA SR1 SYNCML SYNCMLSERV ACTIVESYNC HOTSYNC PALMOS NOKID PCSUITE NFTP NSYNCML NGAGE APPLE IAP ISYNC GATT 

### Try to connect

```shell
# trust a device
[bluetooth]# trust [mac address]

# pair a device
[bluetooth]# pair [mac address]

# list paired devices
[bluetooth]# paired-devices

# connect to device
[bluetooth]# connect [mac address]

# remove a device
[bluetooth]# remove [mac address]
```

Connect with `gattool`.

```shell
# start interactive session
$ sudo gatttool -b 4D:87:5D:55:2F:31 -I

# connect to LE device
[4D:87:5D:55:2F:31][LE]> connect
Attempting to connect to 4D:87:5D:55:2F:31

# show the primary UUIDs
[4D:87:5D:55:2F:31][LE]> primary

# show all available handles
[4D:87:5D:55:2F:31][LE]> char-desc

# exit gattool
[4D:87:5D:55:2F:31][LE]> exit
```

### Info

Sometimes the connect command does not work (_e.g. speakers_), in such cases you can try to install a GUI and the package `pulseaudio-module-bluetooth`.

```shell
...
Failed to connect: org.bluez.Error.Failed
[bluetooth]# exit

# install package
$ sudo apt install -y pulseaudio-module-bluetooth
```

## Start to dump

The `hcidump` utility allows the monitoring of Bluetooth activity. It provides a disassembly of the Bluetooth traffic.

```shell
# start LE scan (if no connection is established)
$ sudo hcitool lescan
```

For example with a 2nd SSH connection you can run `hcidump`.

```shell
# show help (optional)
$ hcidump --help

# dump data in raw
$ sudo hcidump --raw

# dump data in ascii
$ sudo hcidump --ascii

# dump data in ascii and raw
$ sudo hcidump --ext
```

[Go Back](../readme.md)
