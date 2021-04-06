#

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

## Install Ubertooth tools

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

[Go Back](../readme.md)
