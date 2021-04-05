# BeEF

...

## Objective

...

## Install needed and/or optional packages

Install (or ensure they are installed) following packages.

```shell
# update system (optional)
$ sudo apt update -y && sudo apt upgrade -y

# install optional packages (optional)
$ sudo apt install -y vim tree

# install needed packages
$ sudo apt install -y curl git ruby-full
```

## GCC-9

_Note: the following steps (e.q. scp, make) will take a very long time._

```shell
┌──[lupin@macOS]::[~/Desktop]
└─ % curl http://ftp.mirrorservice.org/sites/sourceware.org/pub/gcc/releases/gcc-9.3.0/gcc-9.3.0.tar.gz -o gcc-9.3.0.tar.gz

┌──[lupin@macOS]::[~/Desktop]
└─ % tar zxf gcc-9.3.0.tar.gz 

┌──[lupin@HackMac]::[~/Desktop]
└─ % scp -r gcc-9.3.0 Raspi:/home/pi/

┌──[lupin@HackMac]::[~/Desktop]
└─ % ssh Raspi

#
$ cd gcc-9.3.0

#
$ ./contrib/download_prerequisites

#
$ ./configure --disable-multilib

#
$ make -j 4

#
$ sudo make install

#
$ sudo reboot

#
$ gcc --version
```

## BeEF

...

```shell
#
$ cd ~

#
$ git clone https://github.com/beefproject/beef.git

#
$ cd beef/

#
$ sudo ./install
```

...

[Go Back](./README.md)
