# BeEF on Raspberry PI

...

## Objective

...

## Install needed and/or optional packages

Install (_or ensure they are installed_) following packages.

```shell
# update system (optional)
$ sudo apt update -y && sudo apt upgrade -y

# install optional packages (optional)
$ sudo apt install -y vim

# install needed packages
$ sudo apt install -y curl git build-essential openssl libreadline6-dev zlib1g zlib1g-dev libssl-dev libyaml-dev libsqlite3-0 libsqlite3-dev sqlite3 libxml2-dev libxslt1-dev autoconf libc6-dev libncurses5-dev automake libtool bison nodejs libcurl4-openssl-dev
```

## Install BeEF

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

On line 106 are two packages which are not available `gcc-9-base` and `libgcc-9-dev`. You must remove them from `/home/pi/beef/install`!

```shell
...
if [ "${Distro}" = "Debian" ] || [ "${Distro}" = "Kali" ]; then
   sudo apt-get update
   sudo apt-get install curl git build-essential openssl libreadline6-dev zlib1g zlib1g-dev libssl-dev libyaml-dev libsqlite3-0 libsqlite3-dev sqlite3 libxml2-dev libxslt1-dev autoconf libc6-dev libncurses5-dev automake libtool bison nodejs libcurl4-openssl-dev gcc-9-base libgcc-9-dev
...
```

To save a lot of time, you can add `--no-document` into commmand `sudo gem${RUBYSUFFIX} update --system` on line 205.

## BeEF configuration

Just change username and password on `/home/pi/beef/config.yaml`.

```shell
# modify config.yaml
$ vim config.yaml
```

## Start BeEF

```shell
# start BeEF
$ ./beef
```



