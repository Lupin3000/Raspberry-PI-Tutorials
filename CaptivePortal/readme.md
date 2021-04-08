# Create a Raspberry PI Captive Portal

After you have set up the Wi-Fi access point on the Raspberry PI, you may also need a Captive Portal. The Captive Portal will be shown to STA's directly after they connected to your Wi-Fi, like in Hotels, Airports, public Hotspots, etc. The problem with this is that people can copy such Captive Portals and gather sensible information (_e.g. login credentials_).

## Objective

The aim of this tutorial is to set up a simple (_open_) captive portal in few minutes and to show how you can modify the specific web pages.

## Precondition

You should already have read (_and successful carried out_) the following tutorials.

- [Setup Raspberry PI](../Setup)
- [Prepare Raspberry PI](../Preparation)
- [Wi-Fi Analysis](../WIFIAnalysis)
- [Simple Access Point](../AccessPoint)

## Install needed and/or optional packages

Install (_or ensure they are installed_) following packages.

```shell
# update system (optional)
$ sudo apt update -y && sudo apt upgrade -y

# install optional packages (optional)
$ sudo apt install -y vim tree

# install needed packages
$ sudo apt install -y git build-essential libmicrohttpd-dev
```

## NoDogSplash

### Install NoDogSplash

```shell
# change into home directory
$ cd ~

# clone Github repository
$ git clone https://github.com/nodogsplash/nodogsplash.git

# change into cloned directory
$ cd nodogsplash/

# run make
$ make

# run make and install
$ sudo make install
```

_Note: read this [documentation pages](https://nodogsplashdocs.readthedocs.io/en/stable/) for more information._

### Configure NoDogSplash

```shell
# backup default nodogsplash configuration (optional)
$ sudo mv /etc/nodogsplash/nodogsplash.conf /etc/nodogsplash/nodogsplash.conf.bak

# modify dhcpcd configuration
$ sudo vim /etc/nodogsplash/nodogsplash.conf
```

Uncomment and/or add the following lines in `/etc/nodogsplash/nodogsplash.conf` configuration file.

```
# Gateway interface
GatewayInterface wlan1

# Gateway name
GatewayInterface WuTangLan

# Gateway address
GatewayAddress 192.168.0.1

# Status page
StatusPage status.html

# Spalsh page
SplashPage splash.html

# Redirect url
RedirectURL https://google.com

# Max clients
MaxClients 100
```

Now you modify `/etc/nodogsplash/htdocs/splash.html` and `/etc/nodogsplash/htdocs/status.html`. If you don't like to provide your own content now, you can skip this step.

```shell
$ sudo tree /etc/nodogsplash/htdocs/
├── images
│ └── splash.jpg
├── splash.css
├── splash.html
└── status.html

# backup default nodogsplash splash.html (optional)
$ sudo mv /etc/nodogsplash/htdocs/splash.html /etc/nodogsplash/htdocs/splash.html.bak

# backup default nodogsplash status.html (optional)
$ sudo mv /etc/nodogsplash/htdocs/status.html /etc/nodogsplash/htdocs/status.html.bak
```

The example content for `splash.html`.

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <title>$gatewayname</title>
</head>
<body>
  <div>
    <h1>Welcome to $gatewayname</h1>
    <p><a href="$authtarget" target="_self">ENTER NOW</a></p>
  </div>
</body>
</html>
```

The example content for `status.html`.

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <title>$gatewayname</title>
</head>
<body>
  <div>
    <p>You are already logged in and have access to the Internet.</p>
  </div>
</body>
</html>
```

### Start NoDogSplash

```shell
# copy service file into /lib/systemd/system
$ sudo cp ~/nodogsplash/debian/nodogsplash.service /lib/systemd/system/

# start nodogsplash service
$ sudo systemctl start nodogsplash

# enable nodogsplash service
$ sudo systemctl enable nodogsplash

# check status of nodogsplash service (optional)
$ sudo systemctl status nodogsplash
```

## Debug

If something don't work, following commands will help. Also check your configuration files again! Sometimes errors creep into the IP addresses.

```shell
# show status of service
$ systemctl status nodogsplash
$ ps ax | grep nodogsplash
```

**macOS**

Sometimes macOS does not open the Captive Portal (_for example if you have modified the default DNS settings_), you can try `http://captive.apple.com` or `http://192.168.0.1`.

## Additional

_Note: like the first in first part, this tutorial did not go into more depth on security (e.g. os hardening, firewall, etc.)!_

[Go Back](../readme.md)
