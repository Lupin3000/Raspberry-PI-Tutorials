# Bash Monitor Mode

With a small Bash script, you can save time to set your Wi-Fi interfaces into Monitor Mode.

## Objective

The aim of this tutorial is to set the Wi-Fi interface into Monitor Mode.

## Install needed and/or optional packages

Install (_or ensure they are installed_) following packages.

```shell
# update system (optional)
$ sudo apt update -y && sudo apt upgrade -y

# install optional packages (optional)
$ sudo apt install -y wireless-tools

# install needed packages
$ sudo apt install -y curl
```

## Download and prepare Bash script

```shell
# change into home directory
$ cd ~

# download bash script
$ curl -L https://raw.githubusercontent.com/Lupin3000/Raspberry-PI-Tutorials/main/Goodies/BashMonitorMode/monitor-mode.sh -o monitor-mode.sh

# set file permissions
$ chmod u+x monitor-mode.sh
```

## Enable Monitor Mode

```shell
# show help (optional)
$ ./monitor-mode.sh -h

# enable monitor mode
$ sudo ./monitor-mode -i wlan1
```

[Go Back](../../readme.md)
