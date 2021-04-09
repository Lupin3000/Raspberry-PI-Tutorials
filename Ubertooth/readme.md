# Ubertooth One

...

## Objective

...

## Install needed and/or optional packages

Install (_or ensure they are installed_) following packages.

```shell
# update system (optional)
$ sudo apt update -y && sudo apt upgrade -y

# install optional packages (optional)
$ sudo apt install -y vim

# install needed packages
$ sudo apt install -y cmake libusb-1.0-0-dev make gcc g++ libbluetooth-dev wget pkg-config python3-numpy python3-distutils python3-setuptools python3-qtpy
```

## Install libbtbb

...

```shell
# change into home directory
$ cd ~

# download archive
$ curl -L -C - https://github.com/greatscottgadgets/libbtbb/archive/2020-12-R1.tar.gz -o libbtbb.tar.gz

# extract archive
$ tar -xf libbtbb.tar.gz

# create sub directories and change into
$ mkdir libbtbb-2020-12-R1/build && cd libbtbb-2020-12-R1/build

# create Makefile
$ cmake ..

# start build
$ make

# start installation
$ sudo make install

# configure dynamic linker run-time bindings
$ sudo ldconfig
```

## Ubertooth

### Install Ubertooth tools

...

```shell
# change into home directory
$ cd ~

# download archive
$ curl -L -C - https://github.com/greatscottgadgets/ubertooth/releases/download/2020-12-R1/ubertooth-2020-12-R1.tar.xz -o ubertooth.tar.xz

# extract archive
$ tar -xf ubertooth.tar.xz

# create sub directories and change into
$ mkdir ubertooth-2020-12-R1/host/build && cd ubertooth-2020-12-R1/host/build

# create Makefile
$ cmake ..

# build applications
$ make

# install applications
$ sudo make install

# configure dynamic linker run-time bindings
$ sudo ldconfig
```

### Ubertooth Firmware update

...

```shell
# list USB devices (optional)
$ lsusb | grep Ubertooth
Bus 001 Device 014: ID 1d50:6002 OpenMoko, Inc. Ubertooth One

# show current version
$ ubertooth-util -v
Firmware version: 2015-10-R1 (API:1.01)

# change into home directory
$ cd ~

# change directory
$ cd ubertooth-2020-12-R1/ubertooth-one-firmware-bin

# run firmware update
$ sudo ubertooth-dfu -d bluetooth_rxtx.dfu -r
```

I've got an error `control message unsupported`.

```shell
# re-attach device
$ ubertooth-util -r

# execute firmware update again
$ sudo ubertooth-dfu -d bluetooth_rxtx.dfu -r
Switching to DFU mode...
Checking firmware signature
........................................
........................................
........................................
........
control message unsupported

# show version
$ sudo ubertooth-util -vV
Firmware version: 2020-12-R1 (API:1.07)
ubertooth 2020-12-R1 (mikeryan@steel) Fri Dec 25 13:55:05 PST 2020
```

All good ;) ... I could really confirm that the firmware update was successful.

### Scan with Ubertooth

...

[Go Back](../readme.md)
