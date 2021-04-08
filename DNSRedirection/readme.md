# DNS hijacking, DNS poisoning or DNS redirection

Since Dnsmasq is already running on the Raspberry PI, it is very easy to forward (_unprotected or poorly configured_) STA's to wrong IP's. Through the various DNS or HTTP(S) analyzes, you also know which domains are being accessed by clients.

## Objective

The aim of this tutorial is to set up quickly a simple DNS redirection.

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

## Install needed and/or optional packages

Install (_or ensure they are installed_) following packages.

```shell
# update system (optional)
$ sudo apt update -y && sudo apt upgrade -y

# install optional packages (optional)
$ sudo apt install -y vim

# install needed packages
$ sudo apt install -y lighttpd
```

_Note: You could use also use any other common known web server (like Apache, Nginx, etc.) or Build-in web server (like Python, PHP, etc.)._

## Additional preparation

In case you have NoDogSplash service running, I recommend stopping it (_for now_).

```shell
# stop nodogsplash service
$ sudo systemctl stop nodogsplash.service
```

## lighttpd

After successful installation the web server is already started, and you can visit with your browser the "Placeholder page" via `http://raspberrypi.local` or `http://<ip>`. But you should re-configure some default settings first.

### Configure lighttpd

```shell
# show lighttpd.conf (optional)
$ sudo cat /etc/lighttpd/lighttpd.conf

# show placeholder page (optional)
$ sudo cat /var/www/html/index.lighttpd.html

# list directories (optional)
$ sudo ls -la /var/www/

# show group file (optional)
$ sudo cat /etc/group | grep 'www-data'

# show passwd file (optional)
$ sudo cat /etc/passwd | grep 'www-data'

# change file owner and group recursive
$ sudo chown -R www-data:www-data /var/www/html

# add pi user to group www-data
$ sudo usermod -G www-data -a pi

# change permissions recursive
$ sudo chmod -R 775 /var/www/html
```

### Restart lighttpd

```shell
# reload lighttpd
$ sudo service lighttpd force-reload
```

## Create the fake web page

```shell
# create index.html
$ vim /var/www/html/index.html
```

The content of `/var/www/html/index.html`.

```html
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <title>Fake Page</title>
</head>
<body>
  <div>
    <p>Fake page...</p>
  </div>
</body>
</html>
```

Open again `http://raspberrypi.local` inside your browser, you should see now the content of `index.html`.

## Reconfigure Dnsmasq

### Use the hosts file

There are various options with Dnsmasq to redirect DNS requests. The real simplest one is via `/etc/hosts`. But you have to check again whether this file is read by Dnsmasq. Check the configuration for this `/etc/dnsmasq.conf`!

```dnsmasq.conf
# do not read hosts file (optional)
# no-hosts
```

Add another entry into `/etc/hosts`.

```shell
# modify hosts file
$ sudo vim /etc/hosts
```

Example entry.

```
192.168.0.1             example.com
```

_Note: If you have already called up the domain, you can now wait a little or delete the DNS cache. Otherwise, the real website will still be displayed!_

### Use the addn-hosts

Another way to do this attack with Dnsmasq is as follows.

```shell
# modify dnsmasq configuration
$ sudo vim /etc/dnsmasq.conf

# add spoof.hosts file
$ sudo vim /etc/dnsmasq.d/spoof.hosts

# restart dnsmasq service
$ sudo systemctl restart dnsmasq
```

Add the following lines in `/etc/dnsmasq.conf` configuration file.

```
addn-hosts=/etc/dnsmasq.d/spoof.hosts
```

Add the following lines in `/etc/dnsmasq.d/spoof.hosts` file. It uses the same format as `/etc/hosts`.

```
192.168.0.1 www.example.com example.com
```

_Note: There are some more possibilities with Dnsmasq, just search for it._

## Additional

If the STA is using Domain Name System Security Extensions (_DNSSEC_) technologies or VPN, this attack will not work!

[Go Back](../readme.md)
