# Create a Raspberry PI Captive Portal

After you have set up the Wi-Fi [access point](./RaspberryPI_AccessPoint.md) on the Raspberry PI, you may also need a Captive Portal. Here are instructions for doing this. These steps can also be completed in a few minutes.

## Prerequisite

You should already have set up and started the Wi-Fi access point.

## Objective

The aim of this tutorial is to set up a simple (_open_) captive portal.

## Install needed and/or optional packages

Install (_or ensure they are installed_) following packages.

```shell
# update system (optional)
$ sudo apt update -y && sudo apt upgrade -y

# install optional packages (optional)
$ sudo apt install -y vim tree

# install needed packages
$ sudo apt install -y git build-essential libmicrohttpd-dev

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

## Modify NoDogSplash

```shell
# backup default nodogsplash configuration (optional)
$ sudo mv /etc/nodogsplash/nodogsplash.conf /etc/nodogsplash/nodogsplash.conf.bak

# modify dhcpcd configuration
$ sudo vim /etc/nodogsplash/nodogsplash.conf
```

Uncomment and/or add the following lines in `/etc/nodogsplash/nodogsplash.conf` configuration file.

```nodogsplash.conf
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

# Redirect URL
RedirectURL https://google.com

# MaxClients
MaxClients 100
```

_Note: read this [documentation pages](https://nodogsplashdocs.readthedocs.io/en/stable/) for more informations._

Now you modify `/etc/nodogsplash/htdocs/splash.html` and `/etc/nodogsplash/htdocs/status.html`. If you don't like to provide your own content now, you can skip this step.

```shell
$ sudo tree /etc/nodogsplash/htdocs/
├── images
│   └── splash.jpg
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

Start and test the nodogsplash service.

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
$ systemctl status nodogsplash
$ ps ax | grep nodogsplash
```

**macOS**

Sometimes macOS does not open the Captive Portal (_for example if you have modified the default DNS settings_), you can try `http://captive.apple.com` or `http://192.168.0.1`.

## Additional

Note like the first in first part, this tutorial did not go into more depth on security (_e.g. os hardening, firewall, etc._)!

[Go Back](./README.md)
