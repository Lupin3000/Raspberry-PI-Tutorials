# HTTPS Analysis

Since most traffic nowadays is encrypted, you can try a little trick to bypass this protection. The idea is, clients do connect to you with one of your own certificates what enables you to analyze encrypted traffic.

## Objective

The aim is to analyze the HTTPS traffic from connected STA's where for example `HSTS` web security policy mechanism or other protections are not in use.

## Install needed and/or optional packages

Install (_or ensure they are installed_) following packages.

```shell
# update system (optional)
$ sudo apt update -y && sudo apt upgrade -y

# install optional packages (optional)
$ sudo apt install -y vim tree

# install needed packages
$ sudo apt install -y iptables sslsplit
```

## sslsplit

_Note: Read this [document](https://www.roe.ch/SSLsplit) for more informations._

### Create configuration

Many online search results end up with a very long command line options for sslsplit, don't do that (_just create your own configuration(s) file(s)_)!

```shell
# read configuration sample (optional)
$ sudo /usr/sslsplit/sslsplit.conf.sample

# add own sslsplit configuration
$ sudo vim /usr/sslsplit/sslsplit.conf
```

Add the following lines in `/usr/sslsplit/sslsplit.conf` configuration file (_modify later for your needs_).

```sslsplit.conf
# CA cert (equivalent to -c option)
CACert /usr/sslsplit/ca.crt

# CA key (equivalent to -k option)
CAKey /usr/sslsplit/ca.key

# Connect log (equivalent to -l)
ConnectLog /var/log/sslsplit/connect.log

# Content log (equivalent to -L option (excludes -S/-F))
ContentLog /var/log/sslsplit/content.log

# Log master keys in SSLKEYLOGFILE format (equivalent to -M option)
MasterKeyLog /var/log/sslsplit/masterkeys.log

# Debug mode run in foreground (equivalent to -D option)
Debug yes

# Daemon mode: run in background (equivalent to -d option)
# Daemon yes

# Passthrough SSL connections (equivalent to -P option)
# Passthrough yes

# Proxy specifications (ipv4)
# ProxySpec http 192.168.0.1 8080
# ProxySpec https 192.168.0.1 8443

# Proxy specifications (ipv4)
# ProxySpec http ::ffff:c0a8:1 8080
# ProxySpec https ::ffff:c0a8:1 8443
```

_Note: read this [manual page](https://mirror.roe.ch/rel/sslsplit/sslsplit-0.5.5.conf.5.txt) for more informations._

### Generate self signed certifcate

```shell
# show openssl.cnf (optional)
$ sudo cat /usr/lib/ssl/openssl.cnf
```

Next to all other content inside `/usr/lib/ssl/openssl.cnf`, ensure the following options are set.

```openssl.cnf
[ req ]

distinguished_name	= req_distinguished_name

[ v3_ca ]

subjectKeyIdentifier=hash
authorityKeyIdentifier=keyid:always,issuer
basicConstraints = critical,CA:true
```

Generate key and certificate with `OpenSSL`.

```shell
# show version (optional)
$ openssl version

# show help (optional)
$ openssl help

# generate key
$ sudo openssl genrsa -out /usr/sslsplit/ca.key 4096

# generate certificate
$ sudo openssl req -new -x509 -key /usr/sslsplit/ca.key -out /usr/sslsplit/ca.crt -config /usr/lib/ssl/openssl.cnf -extensions v3_ca -subj '/O=SSLsplit Root CA/CN=SSLsplit Root CA/' -set_serial 0 -days 3650

# show content of directory (optional)
$ sudo tree /usr/sslsplit/
├── ca.crt
├── ca.key
├── sslsplit.conf
└── sslsplit.conf.sample
```

### Add iptables rules

Route the traffic from specific ports over to sslsplit (_listening on port 8443 or port 8080_)

```shell
# save current iptables rules
$ iptables-save > /usr/sslsplit/rules/saved

# http/https iptable rules
$ sudo iptables -t nat -A PREROUTING -p tcp --dport 80 -j REDIRECT --to-ports 8080
$ sudo iptables -t nat -A PREROUTING -p tcp --dport 443 -j REDIRECT --to-ports 8443

# some other rules (optional)
$ sudo iptables -t nat -A PREROUTING -p tcp --dport 587 -j REDIRECT --to-ports 8443
$ sudo iptables -t nat -A PREROUTING -p tcp --dport 465 -j REDIRECT --to-ports 8443
$ sudo iptables -t nat -A PREROUTING -p tcp --dport 993 -j REDIRECT --to-ports 8443
$ sudo iptables -t nat -A PREROUTING -p tcp --dport 5222 -j REDIRECT --to-ports 8080
```

_Note: You could also save the iptables-save, iptables rules, iptables clean-up and iptables-restore as bash script!_

Start sslsplit (_and optional tail_).

```shell
# tail all logfiles (optional)
$ sudo tail -f /var/log/sslsplit/connect.log /var/log/sslsplit/content.log /var/log/sslsplit/masterkeys.log

# start for http/https only
$ sudo sslsplit -f /usr/sslsplit/sslsplit.conf -P https 192.168.0.1 8443 http 192.168.0.1 8080

# start for ssl/tcp
$ sudo sslsplit -f /usr/sslsplit/sslsplit.conf -P ssl 0.0.0.0 8443 tcp 0.0.0.0 8080
```

When you are ready press `CTRL` + `c`, restore your iptables rules and start traffic analysis.

```shell
# clean iptables
$ iptables -F
$ iptables -X
$ iptables -t nat -F
$ iptables -t nat -X
$ iptables -t mangle -F
$ iptables -t mangle -X
$ iptables -P INPUT ACCEPT
$ iptables -P FORWARD ACCEPT
$ iptables -P OUTPUT ACCEPT

# restore iptables rules
$ iptables-restore < /usr/sslsplit/rules/saved

# show content.log
$ sudo cat /var/log/sslsplit/content.log

# show connect.log
$ sudo cat /var/log/sslsplit/connect.log
```

## Important

Many modern browsers protect such kind of analysis and clients will see a warning (_e.q. untrusted certificate_)! For your own needs, transfer the certificate `/usr/sslsplit/ca.crt` from the Raspberry Pi to the client device (_import into browser_).

[Go Back](./README.md)
