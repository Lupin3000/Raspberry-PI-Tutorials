# HTTPS Analysis

...

## Objective

The aim is to analyze the HTTPS traffic from connected STA's where the `HSTS` web security policy mechanism is not in use.

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

```shell
# modify sslsplit configuration
$ sudo vim /usr/sslsplit/sslsplit.conf
```

Add the following lines in `/usr/sslsplit/sslsplit.conf` configuration file.

```sslsplit.conf
# CA cert (equivalent to -c option)
CACert /usr/sslsplit/ca.crt

# CA key (equivalent to -k option)
CAKey /usr/sslsplit/ca.key

# Connect log (equivalent to -l)
ConnectLog /var/log/sslsplit/connect.log

# Content log (equivalent to -L option)
ContentLog /var/log/sslsplit/content.log

# Log master keys in SSLKEYLOGFILE format (equivalent to -M option)
MasterKeyLog /var/log/sslsplit/masterkeys.log

# Debug mode run in foreground (equivalent to -D option)
Debug yes

# Passthrough SSL	connections if they cannot be split (equivalent to -P option)
Passthrough true
```

_Note: read this [manual page](https://mirror.roe.ch/rel/sslsplit/sslsplit-0.5.5.conf.5.txt) for more informations._

### Generate certifcate

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

### iptables

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

_Note: You can save the iptables rules (e.q. as bash script)!_

Start sslsplit (_and optional tail_).

```shell
# tail all logfiles (optional)
$ sudo tail -f /var/log/sslsplit/connect.log /var/log/sslsplit/content.log /var/log/sslsplit/masterkeys.log

# start for http/https
$ sudo sslsplit -f /usr/sslsplit/sslsplit.conf https 192.168.0.1 8443 http 192.168.0.1 8080

# start for ssl/tcp
$ sudo sslsplit -f /usr/sslsplit/sslsplit.conf ssl 0.0.0.0 8443 tcp 0.0.0.0 8080
```

When you are ready.

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
```

## Important

Many modern browser protect this action and clients will see only a warning! For your own needs, transfer the certificate `/usr/sslsplit/ca.crt` from the Raspberry Pi to the client device (_import into browser_).

[Go Back](./README.md)
