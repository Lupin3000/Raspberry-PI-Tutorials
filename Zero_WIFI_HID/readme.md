# Raspberry Pi Zero (W/WH) - USB HID

The Raspberry PI Zero can get enough power via USB, and it can be configured, with few steps, as an OTG (_On-The-Go_) USB device. That's awesome, because you can do similar things like [USB Rubber Ducky](https://shop.hak5.org/products/usb-rubber-ducky-deluxe) with it.

## Objective

The aim of this tutorial is to use the Raspberry PI Zero as USB Keyboard (_HID_).

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
$ sudo apt install -y vim curl tree
```

## Human Interface Device (HID)

### Enable USB On-The-GO (OTG)

```shell
# backup config.txt (optional)
$ sudo cp /boot/config.txt ~/boot-config.txt.bak

# enable dwc2 USB driver
$ echo "dtoverlay=dwc2" | sudo tee -a /boot/config.txt

# backup modules (optional)
$ sudo cp /etc/modules ~/etc-modules.bak

# enable dwc2 in Raspbian
$ echo "dwc2" | sudo tee -a /etc/modules

# enable libcomposite in Raspbian
$ echo "libcomposite" | sudo tee -a /etc/modules
```

[Here](https://www.raspberrypi.org/documentation/configuration/device-tree.md) you will find some information about the Raspberry `Device Tree`.

### Add libcomposite configuration on boot

In order to have the libcomposite configuration run when the Raspberry boots, you simply add the command to file `/etc/rc.local`.

```shell
# backup rc.local (optional)
$ sudo cp /etc/rc.local ~/etc-rc.local.bak

# add new content in rc.local (before exit 0)
$ sudo sed -i '/^exit 0.*/i /usr/bin/hid_usb' /etc/rc.local
```

### Creating the libcomposite configuration (Bash script)

In order to create the device (_USB Linux Gadget_) which has a UDC (_USB Device Controller_), create a libcomposite configuration.

```shell
# download file from GitHub
$ curl -L https://raw.githubusercontent.com/Lupin3000/Raspberry-PI-Tutorials/main/Zero_WIFI_HID/hid_usb -o ~/hid_usb

# copy file to specific target
$ sudo cp ~/hid_usb /usr/bin/hid_usb

# set file permissions
$ sudo chmod +x /usr/bin/hid_usb

# modify content for needs (optional)
$ sudo vim /usr/bin/hid_usb
```

[Here](./hid_usb) you will see the content of the libcomposite configuration `/usr/bin/hid_usb` for the english keyboard.

### Reboot and verify

```shell
# reboot system
$ sudo reboot
```

> Before you restart the Raspberry PI Zero, you have to change the USB port! So do not use the USB port for power anymore. In addition, make sure that you have another device (_for SSH_) ready.

```shell
# confirm /dev/hidg0 (optional)
$ sudo ls -la /dev/hidg0

# confirm /sys/kernel/config/usb_gadget/hid_usb/ (optional)
$ sudo tree /sys/kernel/config/usb_gadget/hid_usb/
├── bcdDevice
├── bcdUSB
├── idProduct
├── idVendor
├── configs
│ └── c.1
│     ├── MaxPower
│     └── strings
│         └── 0x409
│             └── configuration
├── functions
│ └── hid.usb0
│     ├── protocol
│     ├── report_length
│     └── subclass
├── strings
│   └── 0x409
│   ├── manufacturer
│   ├── product
│   └── serialnumber
└── UDC
```

_Note: The command line tree is shortened. There are much more directories, files and links!_

```shell
# download file from GitHub
$ curl -L https://raw.githubusercontent.com/Lupin3000/Raspberry-PI-Tutorials/main/Zero_WIFI_HID/hid_fun.sh -o ~/hid_fun.sh

# change file permissions
$ chmod u+x ~/hid_fun.sh
```

[Here](./hid_fun.sh) you will see the content of the bash script.

```shell
# new SSH connection
$ ssh pi@[ip of your Raspberry PI Zero]

# execute bash script
$ sudo ~/hid_fun.sh
```

#### Fix language issues

In the configuration example, the value `0x409` is used. This value is for English (_United States_)!

> In case you like to use a different language, have a look on following short example list.

- `0x402` Bulgarian
- `0x403` Catalan
- `0x41a` Croatian (Standard)
- `0x405` Czech
- `0x406` Danish
- `0x413` Dutch (Standard)
- `0x809` English (UK)
- `0x40b` Finnish
- `0x40c` French (Standard)
- `0xc07` German (Austria)
- `0x407` German (Standard)
- `0x807` German (Switzerland)
- `0x408` Greek
- `0x40e` Hungarian
- `0x40f` Icelandic
- `0x410` Italian (Standard)
- `0x414` Norwegian (Bokmal)
- `0x415` Polish
- `0x816` Portuguese (Standard)
- `0x418` Romanian
- `0x40a` Spanish (Standard)
- `0x41b` Slovak
- `0x424` Slovenian
- `0x41d` Swedish

_Note: Since I don't want to list all available values here, I recommend that you're simply looking for them online._

[Go Back](../readme.md)
