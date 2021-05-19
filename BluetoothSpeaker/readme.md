# Bluetooth Speaker with Raspberry PI

In order to be able to connect the Raspberry Pi (_headless_) to a Bluetooth speaker, you have to make various preparations. This endeavor can quickly become frustrating, so don't give up!

## Objective

The aim of this tutorial is to learn to connect Bluetooth speakers via command line.

## Precondition

You should already have read (_and successful carried out_) the following tutorials.

- [Setup Raspberry PI](../Setup)
- [Prepare Raspberry PI](../Preparation)
- [Bluetooth Basics & Analysis](../Bluetooth)

## Install needed and/or optional packages

Install (_or ensure they are installed_) following packages.

```shell
# update system (optional)
$ sudo apt update -y && sudo apt upgrade -y

# install optional packages (optional)
$ sudo apt install -y vim curl
```

## Preparation

### 1st issue

If you verify the status of the `bluetooth.service`, you may have the issue that the SAP driver initialization failed.

#### Example of 1st issue

```shell
# get status of bluetooth service
$ sudo systemctl status bluetooth.service
...
May 18 17:36:39 raspberrypi bluetoothd[496]: Sap driver initialization failed.
May 18 17:36:39 raspberrypi bluetoothd[496]: sap-server: Operation not permitted (1)
May 18 17:36:39 raspberrypi bluetoothd[496]: Failed to set privacy: Rejected (0x0b)
...
```

#### Solution of 1st issue

SAP (_SIM Access Profile_) can be disabled in most use cases directly in the bluetooth.service.

```shell
# modify file
$ sudo vim /lib/systemd/system/bluetooth.service
```

Add to the `ExecStart` command simply the argument `--noplugin=sap`.

```
ExecStart=/usr/lib/bluetooth/bluetoothd --noplugin=sap
```

Now restart the service and verify the status again.

```shell
# reload all service files
$ sudo systemctl daemon-reload

# restart service
$ sudo systemctl restart bluetooth.service

# get status of bluetooth service
$ sudo systemctl status bluetooth.service
```

### 2nd issue

The 2nd issue to fix is that the user `pi` should be added to the group `bluetooth`. Otherwise, only user `root` can use the `bluetoothctl` command properly.

#### Example of 2nd issue

```shell
pi@raspberrypi:~ $ bluetoothctl 
[bluetooth]# power on
No default controller available

[bluetooth]# agent on
Agent registration enabled

[bluetooth]# default-agent 
No agent is registered
```

#### Solution of 2nd issue

```shell
# add user pi to group bluetooth
$ sudo usermod -G bluetooth -a pi

# verify group (optional)
$ sudo cat /etc/group | grep bluetooth

# reboot (optional)
$ sudo reboot
```

_Note: this step is not needed if you use a GUI (Raspberry Pi OS with desktop)!_

### 3rd issue

As there is no (_GUI_) player, you need some tools to play media files (_e.g. MP3 files_) from command line.

#### Solution of 3rd issue

_Note: This step is only for [Pulseaudio](#Pulseaudio) needed, for [BlueALSA](#BlueALSA) you should use `aplay`!_

```shell
# install package
$ sudo apt install -y sox libsox-fmt-all

# download a mp3 file (optional)
$ curl "https://cdnm.meln.top/mr/Bob%20Marley%20-%20Roots%20rock%20reagge.mp3?session_key=64881459a074106afb3bdf36670fb2f2&hash=b82631d7822e065e953767c362efd167" -o test.mp3

# play mp3 from command line (optional)
$ play test.mp3
```

_Note: in case you like to use VLC, you can do `$ nvlc test.mp3`._

## Pulseaudio

The first approach is to use `Pulseaudio`, in case you already tried and don't like it - jump over to second approach [BlueALSA](#BlueALSA).

```shell
# install package
$ sudo apt install -y --no-install-recommends pulseaudio pulseaudio-module-bluetooth
```

The `pulse` user needs permission to use Bluetooth.

```shell
# modify file
$ sudo vim /etc/dbus-1/system.d/pulseaudio-system.conf
```

Add the following content to file `/etc/dbus-1/system.d/pulseaudio-system.conf`.

```xml
<busconfig>
    <policy user="pulse">
        <allow own="org.pulseaudio.Server"/>
        <allow send_destination="org.bluez"/>
    </policy>
</busconfig>
```

For Bluetooth, you need also to load some driver modules. This can be done via file `/etc/pulse/system.pa`.

```shell
# modify file
$ sudo vim /etc/pulse/system.pa
```

Add following content at the end and save.

```
### Load driver modules for Bluetooth  
.ifexists module-bluetooth-policy.so  
load-module module-bluetooth-policy  
.endif  
 
.ifexists module-bluetooth-discover.so  
load-module module-bluetooth-discover  
.endif
```

Add user `pi` should be added to the groups `pulse-access` and `audio`.

```shell
# add user pi to group pulse-access
$ sudo usermod -G pulse-access,audio -a pi

# verify group (optional)
$ sudo cat /etc/group | grep pulse-access
$ sudo cat /etc/group | grep audio

# reboot (recommended)
$ sudo reboot
```

Connect the speaker, select audio output (_sink_) and play music.

```shell
# trust a device
[bluetooth]# trust [mac address]

# pair a device
[bluetooth]# pair [mac address]

# connect to device
[bluetooth]# connect [mac address]
```

_Note: Please also note the necessary steps from tutorial [Bluetooth Basics & Analysis](../Bluetooth)!_

```shell
# start pulseaudio
$ pulseaudio --start

# list available cards (optional)
$ pactl list cards short

# list available audio sinks
$ pactl list sinks short

# select bluetooth sink
$ pactl set-default-sink 1

# set volume (optional)
$ pactl set-sink-volume 1 60%

# play sound
$ play test.mp3
```

_Note: This process is very unstable and can be super annoying. I do use 2 terminals (1x for bluetoothctl and 1x for pactl)._

## BlueALSA

```shell
# install package
$ sudo apt install -y bluealsa

# start service
$ sudo systemctl start bluealsa.service

# get status (optional)
$ sudo systemctl status bluealsa.service
```

Same as above - connect speaker and play sound.

```shell
# trust a device
[bluetooth]# trust [mac address]

# pair a device
[bluetooth]# pair [mac address]

# connect to device
[bluetooth]# connect [mac address]

# play sound (A2DP)
$ aplay -D bluealsa:HCI=hci0,DEV=[mac address],PROFILE=a2dp test.mp3

# play sound (SCO)
$ aplay -D bluealsa:HCI=hci0,DEV=[mac address],PROFILE=sco test.mp3
```

We come to the somewhat surprising possibility. You can (_depending on the target device_) also spy on what victims are talking about.

```shell
# record sound (SCO)
$ arecord -D bluealsa:HCI=hci0,DEV=[mac address],PROFILE=sco spy.wav
```

Since many people take for example, AirPods with them to the office, it becomes critical at this point. These Bluetooth devices mostly use BLE (_AKA Bluetooth Smart_) and do not offer/need a pairing PIN option. ... What a world!

[Go Back](../readme.md)
