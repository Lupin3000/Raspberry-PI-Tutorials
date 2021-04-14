# Backup Raspberry PI (SD card) on macOS

If you have made major configuration errors, and you don't always want to restart, or you want to distribute the current status to other cards, you need a backup.

## Objective

The aim of this tutorial is to show the command line possibility of creating a backup.

## Create backup

> Danger! You could make your system unusable if you don't know exactly what you are doing. If you are not 100% sure - fingers away!

### Identify Raspberry SD Card

In my example, I use 32 GB SD Card, so the output of value `size`, boot partition and `external` is already the first hint.

```shell
# change directory (may to Desktop)
┌──[lupin@macOS]::[~]
└─ % cd ~/Desktop/

# show help (optional)
┌──[lupin@macOS]::[~/Desktop]
└─ % diskutil

# list all disks incl. partitions
┌──[lupin@macOS]::[~/Desktop]
└─ % diskutil list
...
/dev/disk4 (external, physical):
   #:                       TYPE NAME                    SIZE       IDENTIFIER
   0:     FDisk_partition_scheme                        *31.9 GB    disk4
   1:             Windows_FAT_32 boot                    268.4 MB   disk4s1
   2:                      Linux                         31.6 GB    disk4s2
...

┌──[lupin@macOS]::[~/Desktop]
└─ % diskutil info disk4
...
Device / Media Name:       Micro SD/M2
...
Disk Size:                 31.9 GB (31914983424 Bytes) (exactly 62333952 512-Byte-Units)
...
```

### Create the backup

After the identification, you can directly start to create the backup.

```shell
# convert and copy
┌──[lupin@macOS]::[~/Desktop]
└─ % sudo dd bs=8m if=/dev/rdisk4 of=raspi-backup.dmg
```

_Note: Use raw disk (rdisk) instead of disk for removable media. The bs value could be (dependent to SD card) between 4m and 16m._

As dd does not show any output about the progress, you can press the keys `ctrl` + `t`.

### Verify the backup

After a while, the backup will be created.

```shell
# show size (optional)
┌──[lupin@macOS]::[~/Desktop]
└─ % du -h raspi-backup.dmg 
 30G	raspi-backup.dmg
```

[Go Back](../../readme.md)
