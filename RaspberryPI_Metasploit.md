# Metasploit

... work in progress ...

## Objective

The aim of this tutorial is to install Metasploit on Raspberry PI and to provide a tiny introduction.

## Install needed and/or optional packages

Install (_or ensure they are installed_) following packages.

```shell
# update system (optional)
$ sudo apt update -y && sudo apt upgrade -y

# install needed packages
$ sudo apt install -y curl nmap
```

## Preparation

For the Metasploit (_first steps_) section, you can create some folders.

```shell
# create some directories
$ mkdir /var/www/html/{images,styles,data}
```

## Install and start Metasploit

```shell
# download latest install script
$ curl https://raw.githubusercontent.com/rapid7/metasploit-omnibus/master/config/templates/metasploit-framework-wrappers/msfupdate.erb > msfinstall

# change file permissions
$ chmod u+x msfinstall

# start installation
$ sudo ./msfinstall

# start msfconsole
$ msfconsole
```

Start the initial msfconsole (_incl. Metasploit version_), this will also setup your database.

```
Would you like to use and setup a new database (recommended)? y
Initial MSF web service account username? [pi]:
Initial MSF web service account password? (Leave blank for random password):
```

Please store this credentials!!!

## Metasploit (_first steps_)

```shell
# add workspace (and switch)
msf6 > workspace -a first-steps

# executes nmap scan
msf6 > db_nmap 192.168.0.1/24

# list all hosts in the database
msf6 > hosts

# list all services in the database
msf6 > services

# exit msf console
msf6 > exit

# search for available http auxiliaries (optional)
msf6 > search auxiliary name:http

# enable directory scanner
msf6 > use auxiliary/scanner/http/dir_scanner

# show options
msf6 auxiliary(scanner/http/dir_scanner) > options

# set RHOST value
msf6 auxiliary(scanner/http/dir_scanner) > set RHOSTS 192.168.0.1

# run scanner
msf6 auxiliary(scanner/http/dir_scanner) > run
...
[+] Found http://192.168.0.1:80/data/ 404 (192.168.0.1)
[+] Found http://192.168.0.1:80/images/ 404 (192.168.0.1)
[+] Found http://192.168.0.1:80/styles/ 404 (192.168.0.1)
...

# exit msfconsole
msf6 auxiliary(scanner/http/dir_scanner) > quit
```

[Go Back](./README.md)
