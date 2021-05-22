# BLE Encryption with crackle on Raspberry PI

... work in progress ...

## Objective

...

## Precondition

You should already have read (_and successful carried out_) the following tutorials.

- [Setup Raspberry PI](../Setup)
- [Prepare Raspberry PI](../Preparation)
- [Bluetooth Basics & Analysis](../Bluetooth)
- [Ubertooth One Basics](../Ubertooth)

## Install needed and/or optional packages

Install (_or ensure they are installed_) following packages.

```shell
# update system (optional)
$ sudo apt update -y && sudo apt upgrade -y

# install needed packages
$ sudo apt install git libpcap-dev
```

## crackle

### Install crackle

... work in progress ...

```shell
#
$ cd ~

#
$ git clone https://github.com/mikeryan/crackle.git

#
$ cd crackle/

#
$ make

#
$ sudo make install

#
$ ls -la /usr/local/bin | grep crackle
```

...

### Run crackle

```shell
#
$ crackle -h


```

[Go Back](../readme.md)