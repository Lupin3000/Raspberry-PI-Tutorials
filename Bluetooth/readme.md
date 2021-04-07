# Bluetooth Basics and Analysis with Raspberry PI

The Raspberry PI already comes with a Bluetooth device. This is very good because you can achieve a lot with it. Since many Bluetooth device manufacturers want to make the connection as easy as possible for users, you can start with the analysis.

## Objective

The aim of this tutorial is to learn some Bluetooth basics and to start with the Bluetooth analysis.

## Install needed and/or optional packages

Install (_or ensure they are installed_) following packages.

```shell
# update system (optional)
$ sudo apt update -y && sudo apt upgrade -y

# install optional packages (optional)
$ sudo apt install -y bluez
```

## Some basics first

There are already some common tools available on Raspberry PI - for example `hcitool` and `bluetoothctl`.

_Note: As per my knowledge the hcitool is deprecated, I will focus only on bluetoothctl. Of course, you could have a look on the hcitool, too._

### Controller

Some basic commands for the controller.

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

**Scan for devices**

Now already the cool stuff, you start to analyze what devices are around.

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

Wow ... the showed information's are really great. With this information you know already a lot about the device! Store this information and continue with your Bluetooth analysis.

After the scan is stopped, all devices will be deleted soon.

```shell
...
[DEL] Device E8:38:80:7F:E3:D7 root
...
[bluetooth]# info E8:38:80:7F:E3:D7
Device E8:38:80:7F:E3:D7 not available
```

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

## Info

Sometimes the connect command does not work (_e.q. speakers_), in such cases you can try to install a GUI and the package `pulseaudio-module-bluetooth`.

```shell
...
Failed to connect: org.bluez.Error.Failed
[bluetooth]# exit

# install package
$ sudo apt install -y pulseaudio-module-bluetooth
```

[Go Back](../readme.md)
