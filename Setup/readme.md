# Setup Raspberry PI (_headless_)

In order to be able to follow the tutorials better, I would like to quickly show you how to set up the Raspberry PI.

_Note: There are also many other setup options, the one shown here is just a suggestion!_

## Objective

The aim of this tutorial is to show used hardware, and the initial setup of your Raspberry PI.

## Hardware

I use [this hardware](https://www.raspberrypi.org/products/raspberry-pi-4-model-b/?variant=raspberry-pi-4-model-b-8gb) for all tutorials. For many purposes (_but not all_) you can also use previous versions of the Raspberry PI.

## Install Raspberry Pi

The easiest and most comfortable installation is with the `Raspberry Pi Imager`. You can download it [here](https://www.raspberrypi.org/software/) and then install it. As soon as the installation is successfully completed, put the SD card into your SD card into your SD card reader and run Raspberry Pi Imager. First, select the OS (_e.g. Raspberry Pi OS Lite_). Second, select the SD card and third press button `Write`. 

![Raspberry Pi Imager](./RaspberryPI_ImageBuilder.jpg)

> **Raspberry Pi OS Lite**<br>
Release date: March 4th 2021<br>
Kernel version: 5.10<br>
Size: 1175 MB

_Note: In the following tutorials, I do as first step always an update/upgrade. You should also keep your system up-2-date._

## Enable SSH

To enable SSH on headless Raspberry PI, simply create the (_empty_) file named `ssh`, into the boot partition of the SD card.

```shell
# create empty file
┌──[lupin@macOS]::[~]
└─ % touch /Volumes/boot/ssh
```

## Enable Wi-Fi

Similar to SSH you also can set up already the Wi-Fi (_as STA_). Only difference is that this configuration `wpa_supplicant.conf`_ file needs some content.

```shell
# add and modify file
┌──[lupin@macOS]::[~]
└─ % vim /Volumes/boot/wpa_supplicant.conf
```

Add the content to your configuration file (_depending on your location and Wi-Fi_).

```
ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev
update_config=1
country=<Country code>

network={
 ssid="<Name of your Wi-Fi AP>"
 psk="<Password>"
}
```

Unmount the SD card, plug into Raspberry PI and start up the device. After the start, connect with SSH (_user: pi and password: raspberry_) and change to user `root`. As root run the command `raspi-config` and finish your setup.

```shell
# ssh connection to Raspberry PI
┌──[lupin@macOS]::[~]
└─ % ssh pi@raspberry.local

# change to root
$ sudo su -

# start console based raspi-config application
$ raspi-config
```

![raspi-config](./raspi-config.jpg)

_Note: Please activate SSH and set up the Wi-Fi again (_just to ensure_)._

## Additional

From version 1.6, you can save some time (_many configuration steps_) with the advanced option feature. Just hit keys [Ctrl] + [Shift] + [x]!

![Advanced Options](./advanced_options.jpg)

[Go Back](../readme.md)
