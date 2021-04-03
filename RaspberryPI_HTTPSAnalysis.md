# HTTPS Analysis

...

## Objective

The aim is to analyze the HTTPS traffic from connected STA's where the `HSTS` web security policy mechanism is not in use.

## Install needed and/or optional packages

Install (_or ensure they are installed_) following packages.

```shell
# update system (optional)
$ sudo apt update -y && sudo apt upgrade -y

# install needed packages
$ sudo apt install -y vim sslsplit
```

## sslsplit

...

```shell
#
$ sudo vim /usr/sslsplit/sslsplit.conf
```

Add the following lines in `/usr/sslsplit/sslsplit.conf` configuration file.

```sslsplit.conf
# CA cert (equivalent to -c option)
CACert /usr/etc/sslsplit/ca.crt

# CA key (equivalent to -k option)
CAKey /usr/etc/sslsplit/ca.key

# Connect log (equivalent to -l)
ConnectLog /var/log/sslsplit/connect.log

# Content log (equivalent to -L option)
ContentLog /var/log/sslsplit/content.log

# Log master keys in SSLKEYLOGFILE format (equivalent to -M option)
MasterKeyLog /var/log/sslsplit/masterkeys.log

# Debug mode run in foreground (equivalent to -D option)
Debug yes
```

_Note: read this [manual page](https://mirror.roe.ch/rel/sslsplit/sslsplit-0.5.5.conf.5.txt) for more informations._

### Generate certifcate

...

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

...

```shell
#
$ sudo openssl genrsa -out /usr/etc/sslsplit/ca.key 4096

#
$ sudo openssl req -new -x509 -key /usr/etc/sslsplit/ca.key -out /usr/etc/sslsplit/ca.crt -config /usr/lib/ssl/openssl.cnf -extensions v3_ca -subj '/O=SSLsplit Root CA/CN=SSLsplit Root CA/' -set_serial 0 -days 3650
``
$ sudo openssl req -new -x509 -key /usr/etc/sslsplit/ca.key -out /usr/etc/sslsplit/ca.crt -config /usr/lib/ssl/openssl.cnf -extensions v3_ca -subj '/O=SSLsplit Root CA/CN=SSLsplit Root CA/' -set_serial 0 -days 3650
