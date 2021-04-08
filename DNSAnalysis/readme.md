# DNS Analysis with Raspberry PI

Knowing which domains are being requested, means you knowing on which web pages the sensible information is on (_e.q. what content is from interest, credentials, etc._). It can also be used for further attacks.

## Objective

The aim is to analyze the DNS queries from connected STA's and DNS forwards + DNS cache, so that you know which domains get requested.

## Precondition

- [Setup Raspberry PI](../Setup)
- [Prepare Raspberry PI](../Preparation)
- [Wi-Fi Analysis](../WIFIAnalysis)
- [Simple Access Point](../AccessPoint)

## Install needed and/or optional packages

Install (_or ensure they are installed_) following packages.

```shell
# update system (optional)
$ sudo apt update -y && sudo apt upgrade -y

# install needed packages
$ sudo apt install -y vim tcpdump
```

## Analysis with tcpdump

As in a previous tutorial [Wi-Fi Analysis](../WIFIAnalysis), you can use `tcpdump` to analyze the current DNS traffic.

```shell
# show DNS traffic for interface wlan0
$ sudo tcpdump -i wlan0 -nn -l udp port 53

# show DNS traffic for interface wlan1
$ sudo tcpdump -i wlan1 -nn -l udp port 53
```

With the help of `grep` and other Linux standard tools, a more precise filtering is possible.

## Analysis of Dnsmasq log files

I hope you remember when and where you configure the DNS log files! The answer is, you did it in the file `/etc/dnsmasq.conf`.

```shell
$ sudo grep "log" /etc/dnsmasq.conf
# Enable logging
log-queries
log-dhcp
log-facility=/tmp/dnsmasq.log
```

With "vim", "cat", "less", "tail" (_as well as many other tools_) you can view and evaluate the log file.

```shell
# show full content
$ sudo cat /tmp/dnsmasq.log

# show last 10 lines (and follow)
$ sudo tail -f /tmp/dnsmasq.log
```

However, this is a bit cumbersome (_depending on the size of the log file_) and can also be made much easier.

### Create AWK analysis script

```shell
# create new awk file
$ vim dnsmasq.awk
```

The content of `dnsmasq.awk`.

```awk
( $4 ~ /dnsmasq\[[0-9]+\]:/ ) {
  if ( $5 == "query[A]") {
    query[$6]++;
  } else {
    if ( $5 == "forwarded" )
      forwarded[$6]++;
    else
      if ( $5 == "cached" )
        cached[$6]++;
  }
}
END {
  queries=0;
  qforwarded=0
  qacache=0
  printf " %40s |      nb    |  forwarded |  answered from cache \n", "name";
  for (name in query) {
    printf "%s%40s | %9d  | %9d  | %9d\n", \
    ( forwarded[name] > query[name] ? "*" : " "), \
    name, \
    query[name], \
    forwarded[name], \
    cached[name];
    queries += query[name];
    qforwarded += forwarded[name];
    qacache += cached[name];
  }
  printf " %40s | %9d  | %9d  | %9d\n", "total:", queries, qforwarded, qacache;
}
```

Run `dnsmasq.awk` script.

```shell
# execute awk script
$ sudo awk -f dnsmasq.awk /tmp/dnsmasq.log
                                     name |      nb    |  forwarded |  answered from cache
*      configuration.apple.com.akadns.net |         1  |         2  |         0
*                          dpm.demdex.net |         1  |         2  |         0
*                     static.zdassets.com |         1  |         2  |         0
*                   2.debian.pool.ntp.org |         1  |         2  |         0
*                               fbsbx.com |         1  |         2  |         0
...

# execute awk script (and pipe through less)
$ sudo awk -f dnsmasq.awk /tmp/dnsmasq.log | less
```

[Go Back](../readme.md)
