# DNS hijacking, DNS poisoning or DNS redirection

Since Dnsmasq is already running on the Raspberry PI, it is very easy to forward (_unprotected or poorly configured_) STA's to wrong IP's. Through the various DNS or HTTP(S) analyzes, you also know which domains are being accessed by clients.

## Objective

The aim of this tutorial is to setup quickly a simple DNS redirection.

## Install needed and/or optional packages

Install (_or ensure they are installed_) following packages.

```shell
# update system (optional)
$ sudo apt update -y && sudo apt upgrade -y

# install optional packages (optional)
$ sudo apt install -y vim tree

# install needed packages
$ sudo apt install -y lighttpd
```

_Note: You could use also use any other common known web server (like Apache, Nginx, etc.) or Build-in web server (like Python, PHP, etc.)._

## Additional preparation

In case you have NoDogSplash service running, I recommend to stop it (_for now_).

```shell
# stop nodogsplash service
$ sudo systemctl stop nodogsplash.service
```

## lighttpd

After successful installation the web server is already started and you can visit with your browser the "Placeholder page" via `http://raspberrypi.local` or `http://<ip>`. But you should re-configure some default settings first.

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

# reload lighttpd
$ sudo service lighttpd force-reload

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

## Dnsmasq

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

```hosts
192.168.0.1             example.com
```

If you have already called up the domain, you can now wait a little or delete the DNS cache. Otherwise the real website will still be displayed!

[Go Back](./README.md)
