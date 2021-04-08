# STA enumeration with Raspberry PI

In the same way as you can collect information (_e.g. from servers_), you can collect information from connected stations. If you know the operating system and maybe the services (_incl. versions_), you can search for specific vulnerabilities or focus the attack vector later.

## Objective

The aim of this tutorial is to gather information about OS and services (_fingerprint_) by connected STA's.

## Precondition

You should already have read (_and successful carried out_) the following tutorials.

- [Setup Raspberry PI](../Setup)
- [Prepare Raspberry PI](../Preparation)
- [Wi-Fi Analysis](../WIFIAnalysis)
- [Wi-Fi Jamming](../WIFIJamming)
- [Simple Access Point](../AccessPoint)

## Install needed and/or optional packages

Install (_or ensure they are installed_) following packages.

```shell
# update system (optional)
$ sudo apt update -y && sudo apt upgrade -y

# install needed packages
$ sudo apt install -y nmap p0f curl jq
```

## Search connected stations

With a look on the arp cache, you will find very quickly the connected stations incl. the IP and mac address.

```shell
# output arp cache
$ arp -a
...
? (192.168.0.171) at 5a:46:9a:eb:35:2b [ether] on wlan1
? (192.168.0.172) at b7:50:10:a8:dd:3c [ether] on wlan1
? (192.168.0.173) at dc:a6:32:b3:4d:2b [ether] on wlan1
...
```

## Nmap

Nmap is the well-known tool among specialists for network discovery and security auditing.

```shell
# show help (optional)
$ nmap -h

# OS detection, determine service/version info
$ sudo nmap -O -sV 192.168.0.171

# OS detection, version detection, script scanning, and traceroute
$ sudo nmap -A 192.168.0.171

# OS detection on subnet
$ sudo nmap -O 192.168.0.1/24

# OS detection on IP range
$ sudo nmap -O 192.168.0.100-200
```

## p0f

P0f is a passive traffic fingerprinting of TCP/IP communications. The results, after leaving it a while running, are not so bad.

```shell
# show help (optional)
$ p0f -h

# run p0f on interface
$ sudo p0f -i wlan1
...
.-[ 192.168.0.171/53914 -> 172.217.168.35/443 (syn) ]-
| client   = 192.168.0.171/53914
| os       = Mac OS X
| dist     = 0
| params   = generic fuzzy
| raw_sig  = 4:64+0:0:1460:65535,6:mss,nop,ws,nop,nop,ts,sok,eol+1:df,ecn:0
`----
...

# run p0f on interface and log
$ sudo p0f -i wlan1 -o /tmp/p0f.log

# read log file
$ sudo cat /tmp/p0f.log
```

## curl & jq

Via `curl` and `jq` you can try to do a quick OUI lookup, for example on `https://macvendors.co/api` or `https://mac2vendor.com`. 

```shell
# run silent curl request and pipe through jq
$ curl -s 'https://macvendors.co/api/dc:a6:32:b3:4d:2b/json' | jq .
{
  "result": {
    "company": "Raspberry Pi Trading Ltd",
    "mac_prefix": "DC:A6:32",
    "address": "Maurice Wilkes Building, Cowley Road,Cambridge    CB4 0DS,GB",
    "start_hex": "DCA632000000",
    "end_hex": "DCA632FFFFFF",
    "country": null,
    "type": "MA-L"
  }
}

# run silent curl request and pipe through jq
$ curl -s https://mac2vendor.com/api/v4/mac/001451 | jq .
{
  "success": true,
  "results": 1,
  "payload": [
    {
      "vendor": "Apple",
      "mac": {
        "int": 5201,
        "str": "001451",
        "strlower": "001451",
        "strupper": "001451",
        "dot": "00:14:51",
        "dotlower": "00:14:51",
        "dotupper": "00:14:51",
        "dash": "00-14-51",
        "dashlower": "00-14-51",
        "dashupper": "00-14-51"
      }
    }
  ]
}
```

[Go Back](../readme.md)
