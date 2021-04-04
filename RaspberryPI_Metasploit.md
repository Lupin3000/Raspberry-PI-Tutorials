#

...

## Objective

...

## Install needed and/or optional packages

Install (_or ensure they are installed_) following packages.

```shell
# update system (optional)
$ sudo apt update -y && sudo apt upgrade -y

# install needed packages
$ sudo apt install -y curl nmap
```

## Preparation

...

```shell
#
$ mkdir /var/www/html/{images,styles,data}
```

## Install Metasploit

```shell
# download latest install script
$ curl https://raw.githubusercontent.com/rapid7/metasploit-omnibus/master/config/templates/metasploit-framework-wrappers/msfupdate.erb > msfinstall

# change file permissions
$ chmod u+x msfinstall

# start installation
$ sudo ./msfinstall

# show version and finalize installation
$ msfconsole --version
```

Start the initial msfconsole (_incl. Metasploit version_), this will also setup your database.

```
Would you like to use and setup a new database (recommended)? y
Initial MSF web service account username? [pi]:
Initial MSF web service account password? (Leave blank for random password):
```

Please store this credentials!!!

## Start Metasploit

```shell
# start msf console
$ msfconsole

# show the current data service status
msf6 > db_status

# run update
msf6 > msfupdate

# list database workspaces
msf6 > workspace

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
```

...

```shell
# start msf console (without banner)
$ msfconsole -L

# change workspace
msf6 > workspace first-steps

#
msf6 > search auxiliary name:http

#
msf6 > use auxiliary/scanner/http/dir_scanner

#
msf6 auxiliary(scanner/http/dir_scanner) > options

#
msf6 auxiliary(scanner/http/dir_scanner) > set RHOSTS 192.168.0.1

#
msf6 auxiliary(scanner/http/dir_scanner) > run
```

[Go Back](./README.md)
