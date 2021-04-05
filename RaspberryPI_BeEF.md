# BeEF

...

## Objective

...

## Install needed and/or optional packages

Install (_or ensure they are installed_) following packages.

```shell
# update system (optional)
$ sudo apt update -y && sudo apt upgrade -y

# install optional packages (optional)
$ sudo apt install -y vim tree

# install needed packages
$ sudo apt install -y build-essential curl git ruby-full
```

## GCC-9

_Note: the following steps (e.q. scp, make) will take a very long time. I have downloaded and extracted on my macOS (to speed up)._

```shell
┌──[lupin@macOS]::[~/Desktop]
└─ % curl http://ftp.mirrorservice.org/sites/sourceware.org/pub/gcc/releases/gcc-9.3.0/gcc-9.3.0.tar.gz -o gcc-9.3.0.tar.gz

┌──[lupin@macOS]::[~/Desktop]
└─ % tar zxf gcc-9.3.0.tar.gz 

┌──[lupin@macOS]::[~/Desktop]
└─ % scp -r gcc-9.3.0 Raspi:/home/pi/

┌──[lupin@macOS]::[~/Desktop]
└─ % rm -fr gcc-9.3.0 gcc-9.3.0.tar.gz

┌──[lupin@macOS]::[~/Desktop]
└─ % ssh Raspi

# change directory
$ cd gcc-9.3.0

# download required prerequisites
$ ./contrib/download_prerequisites

# run configuration
$ ./configure --disable-multilib

# run build
$ make -j 4

# run install
$ sudo make install

# reboot system
$ sudo reboot

# show gcc version
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
