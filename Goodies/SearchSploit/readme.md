# SearchSploit on Raspberry PI

After the analysis of your network, stations, services, etc. you can go online to [Exploit Database](https://www.exploit-db.com/) and search there for common exploits. But you can do same offline via command line! That's good if you like to save some time or simply don't have an online connection.

## Objective

The aim of this tutorial is to install and use SearchSploit.

## Install needed and/or optional packages

Install (_or ensure they are installed_) following packages.

```shell
# update system (optional)
$ sudo apt update -y && sudo apt upgrade -y

# install needed packages
$ sudo apt install -y git
```

## SearchSploit

### Install SearchSploit

```shell
# clone repository
$ sudo git clone https://github.com/offensive-security/exploitdb.git /opt/exploit-database

# create symbolic link
$ sudo ln -sf /opt/exploit-database/searchsploit /usr/local/bin/searchsploit

# copy rc file into home directory
$ cp -n /opt/exploit-database/.searchsploit_rc ~/

# show rc file (optional)
$ cat ~/.searchsploit_rc

# execute bash rc file
$ source ~/.bashrc
```

### Update SearchSploit

After the installation as well as regularly, you should carry out updates.

```shell
# searchsploit update
$ searchsploit -u
```

_Note: Be patient, this step may take a little longer._

### Using SearchSploit

```shell
# show help (optional)
$ searchsploit -h

# basic search example
$ searchsploit wordpress core 1.2

# basic search example
$ searchsploit smb windows 10

# title search example
$ searchsploit -t android
```

[Go Back](../../readme.md)
