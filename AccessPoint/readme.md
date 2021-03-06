# Create a Raspberry PI Access Point

With the Raspberry PI you can create a Wi-Fi access point (_AP_) in a very short time. It is also known as the Evil Twin or Rogue access point, which mimics legitimate access points.

## Objective

The aim is to create a simple (_open_) access point through 2 Wi-Fi interfaces.

- eth0 (_not used in this tutorial, but simply possible_)
- wlan0 (_Raspberry as STA, internet from Gateway_)
- wlan1 (_provide AP for STA's with network 192.168.0.1/24_)

## Precondition

You should already have read (_and successful carried out_) the following tutorials.

- [Setup Raspberry PI](../Setup)
- [Prepare Raspberry PI](../Preparation)
- [Wi-Fi Analysis](../WIFIAnalysis)
- [Wi-Fi Jamming](../WIFIJamming)

## Install needed and/or optional packages

Install (_or ensure they are installed_) following packages.

```shell
# update system (optional)
$ sudo apt update -y && sudo apt upgrade -y

# install optional packages (optional)
$ sudo apt install -y vim net-tools wireless-tools

# install needed packages
$ sudo apt install -y iptables dhcpcd5 dnsmasq hostapd
```

## dhcpcd

### Configure dhcpcd

```shell
# backup default dhcpcd configuration (optional)
$ sudo mv /etc/dhcpcd.conf /etc/dhcpcd.conf.bak

# modify dhcpcd configuration
$ sudo vim /etc/dhcpcd.conf
```

Uncomment and/or add the following lines in `/etc/dhcpcd.conf` configuration file.

```
# interface configuration
interface wlan1

# static IP (CIDR)
static ip_address=192.168.0.1/24

# don't call the wpa_supplicant hook
nohook wpa_supplicant

# don't send DHCP requests to interface (optional)
# denyinterfaces eth0
```

_Note: read this [manual page](https://www.daemon-systems.org/man/dhcpcd.8.html) for more information._

### Restart dhcpcd

```shell
# restart dhcpcd service
$ sudo systemctl restart dhcpcd

# check status of dhcpcd service (optional)
$ sudo systemctl status dhcpcd
```

## Dnsmasq

### Configure Dnsmasq

```shell
# backup default dnsmasq configuration (optional)
$ sudo mv /etc/dnsmasq.conf /etc/dnsmasq.conf.bak

# modify dnsmasq configuration
$ sudo vim /etc/dnsmasq.conf
```

Add the following lines in `/etc/dnsmasq.conf` configuration file.

```
# listen for DHCP/DNS requests only on specified interfaces
interface=wlan1

# disable DHCP/TFTP on interface
no-dhcp-interface=wlan0

# supply the range of addresses available for lease and lease time
dhcp-range=192.168.0.100,192.168.0.200,255.255.255.0,24h

# DNS
dhcp-option=option:dns-server,192.168.0.1

# enable logging (optional)
log-queries
log-dhcp
log-facility=/tmp/dnsmasq.log

# upstream DNS server addresses
server=8.8.8.8

# do not read hosts file (optional)
# no-hosts

# do not read resolv.conf file (optional)
# no-resolv

# set the cachesize (optional)
# cache-size=150
```

_Note: read this [manual page](https://thekelleys.org.uk/dnsmasq/docs/dnsmasq-man.html) for more information._

### Test and restart Dnsmasq

```shell
# verify dnsmasq configuration (optional)
$ sudo dnsmasq --test -C /etc/dnsmasq.conf

# restart dnsmasq service
$ sudo systemctl restart dnsmasq

# enable dnsmasq service
$ sudo systemctl enable dnsmasq

# check status of dnsmasq service (optional)
$ sudo systemctl status dnsmasq
```

You can read dnsmasq log files (_if enabled_), later if everything works.

```shell
# read log file (optional)
$ sudo tail -f /tmp/dnsmasq.log
```

## Hostapd

### Configure Hostapd

```shell
# create hostapd configuration
$ sudo vim /etc/hostapd/hostapd.conf
```

Add the following lines in `/etc/hostapd/hostapd.conf` configuration file. The value for SSID in my example is `WuTangLan`, change for your needs.

```
# interface
interface=wlan1

# SSID
ssid=WuTangLan

# Channel (optional)
# default: 0, i.e., not set
channel=6

# operation mode
# a = IEEE 802.11a (5 GHz)
# b = IEEE 802.11b (2.4 GHz)
# g = IEEE 802.11g (2.4 GHz)
# ad = IEEE 802.11ad (60 GHz)
# a/g = IEEE 802.11n (HT)
hw_mode=g

# maximum number of stations allowed (optional)
max_num_sta=100

# country code
country_code=CH

# station MAC address -based authentication
# 0 = accept unless in deny list
# 1 = deny unless in accept list
# 2 = use external RADIUS server (accept/deny lists are searched first)
macaddr_acl=0

# send empty SSID in beacons and ignore probe request frames
# 0 disabled
# 1 = send empty
# 2 = clear SSID but keep the original length
ignore_broadcast_ssid=0
```

_Note: read this [manual page](https://nxmnpg.lemoda.net/8/hostapd) for more information._

Change permissions, test and modify hostapd init script.

```shell
# change file permissions
$ sudo chmod 600 /etc/hostapd/hostapd.conf

# test hostapd configuration (optional)
$ sudo hostapd -dd /etc/hostapd/hostapd.conf

# modify hostapd init script
$ sudo vim /etc/default/hostapd
```

Modify the following lines in `/etc/default/hostapd` init script

```
RUN_DAEMON=yes
DAEMON_CONF="/etc/hostapd/hostapd.conf"
```

### Start Hostapd

```shell
# unmasking hostapd service
$ sudo systemctl unmask hostapd

# start hostapd service
$ sudo systemctl start hostapd

# enable hostapd service
$ sudo systemctl enable hostapd

# check status of hostapd service (optional)
$ sudo systemctl status hostapd
```

The default log location is `/var/log/syslog`.

```shell
# read log file (optional)
$ sudo tail -f /var/log/syslog

# read log file and pipe through grep (optional)
$ sudo tail -f /var/log/syslog | grep hostapd
```

## Configure Routing and NAT

```shell
# backup default sysctl configuration (optional)
$ sudo mv /etc/sysctl.conf /etc/sysctl.conf.bak

# modify sysctl configuration
$ sudo vim /etc/sysctl.conf
```

Add the following lines in `/etc/sysctl.conf` configuration file.

```
net.ipv4.ip_forward=1
net.ipv6.conf.all.forwarding=1
```

Add new iptables rules (_store them and reload after the boot_).

```shell
# add new iptables rules
$ sudo iptables -t nat -A POSTROUTING -o wlan0 -j MASQUERADE
$ sudo iptables -A FORWARD -i wlan0 -o wlan1 -m state --state RELATED,ESTABLISHED -j ACCEPT
$ sudo iptables -A FORWARD -i wlan1 -o wlan0 -j ACCEPT

# save iptables firewall rules permanently
$ sudo sh -c "iptables-save > /etc/iptables.ipv4.nat"

# modify rc.local
$ sudo vim /etc/rc.local
```

Add restore iptables commands to run on the startup (_add before exit 0_).

```shell
#!/bin/sh -e
#
# rc.local
#
# This script is executed at the end of each multiuser runlevel.
# Make sure that the script will "exit 0" on success or any other
# value on error.
#
# In order to enable or disable this script just change the execution
# bits.
#
# By default this script does nothing.

# Print the IP address
_IP=$(hostname -I) || true
if [ "$_IP" ]; then
  printf "My IP address is %s\n" "$_IP"
fi

iptables-restore < /etc/iptables.ipv4.nat
exit 0
```

## Reboot Raspberry PI

Restart the Raspberry PI and verify that STA's can connect to your AP (_incl. internet connection_).

```shell
# reboot system
$ sudo reboot
```

## Debug

If something don't work, following commands will help. Also check your configuration files again! Sometimes errors creep into the IP addresses.

```shell
# show IP addresses of specific interfaces
$ ip -4 addr show dev wlan0
$ ip -4 addr show dev wlan1


$ iw phy phy0 info
$ iw phy phy1 info

# show route
$ route
# or
$ ip route list

# show status of specific services
$ systemctl status hostapd
$ ps ax | grep hostapd

$ systemctl status dnsmasq
$ ps ax | grep dnsmasq

$ systemctl status dhcpcd
$ ps ax | grep dhcpcd
```

## Additional

Please also note that the tutorial did not go into more depth on security (_e.g. OS hardening, firewall, etc._)!

[Go Back](../readme.md)
