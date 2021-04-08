# Prepare your Raspberry PI

The content of this document is not an obligation but a recommendation.

## Objective

The aim of this tutorial is to make your daily work easier.

## Precondition

You should already have read (_and successful carried out_) the following tutorials.

- [Setup Raspberry PI](../Setup)

## Change the password of user pi

Everyone knows the default password `raspberry` of the `pi` user, so one of your first action should be to change it!

```shell
# change password
$ passwd
```

## Check if the Raspberry PI is available

To figure out if the Raspberry PI is ready and if you can start the SSH connection, simply check the ARP cache of your system. You don't need to make a ping scan!

```shell
# output arp cache
┌──[lupin@macOS]::[~]
└─ % arp -a
```

## Password-less SSH Login

To save some time and to spare your nerves - it's recommended to use the ssh connection login without a password.

```shell
# create SSH keys
┌──[lupin@macOS]::[~]
└─ % ssh-keygen -t rsa -b 4096

# show content of public key
┌──[lupin@macOS]::[~]
└─ % cat ~/.ssh/id_rsa.pub
```

On Raspberry PI do the follow actions.

```shell
# change into home directory
$ cd ~

# create ssh directory and set permissions
$ mkdir .ssh && chmod 0700 .ssh

# create file authorized_keys and set permissions
$ touch .ssh/authorized_keys && chmod 0644 .ssh/authorized_keys
```

Now add the content of your local file `~/.ssh/id_rsa.pub`.

## Create a SSH configuration

The IP of your Raspberry PI can change after start/reboot and also the SSH command could be very long. This could be easily changed with a simple SSH configuration file.

```shell
# create and modify configuration
┌──[lupin@macOS]::[~]
└─ % vim ~/.ssh/config
```

The example content of SSH configuration file `.ssh/config`.

```
Host *
  Port                22
  Protocol            2
  AddressFamily       inet
  Compression         yes
  IdentityFile        ~/.ssh/id_rsa
  Compression         yes
  ServerAliveInterval 60
  ServerAliveCountMax 3
  TCPKeepAlive        yes
  LogLevel            INFO

Host Raspi
  HostName            raspberrypi.local
  user                pi
```

_Note: Read this [online document](https://www.ssh.com/ssh/config/) to learn more about SSH configurations._

Now you can establish the SSH connection very easily via following the command.

```shell
# ssh into Raspberry PI
┌──[lupin@macOS]::[~]
└─ % ssh Raspi
```

If you know need to copy something (_via SCP_), you can use the host name, too.

```shell
# copy file to Raspberry PI
┌──[lupin@macOS]::[~]
└─ % scp <local file> Raspi:/home/pi/
```

[Go Back](../readme.md)
