#!/usr/bin/env python3

import argparse
import signal
from os import system
from scapy.layers.dot11 import Dot11, Dot11Elt, Dot11Beacon, Dot11ProbeResp, RadioTap, sniff
from sys import exit
from threading import Thread
from time import sleep


def keyboard_interrupt_handler(interrupt_signal, frame):
    print("\nScan stopped")
    # print("KeyboardInterrupt ID: {} {} has been caught.".format(interrupt_signal, frame))
    exit(1)


def change_channel():
    global interface
    channel_number = 1

    while True:
        system(f"iwconfig {interface} channel {channel_number}")
        channel_number = channel_number % 14 + 1
        sleep(0.5)


def set_specific_channel(channel_number):
    global interface

    system(f"iwconfig {interface} channel {channel_number}")


def evaluate_ap_packet(packet):
    if packet.haslayer(Dot11Beacon) or packet.haslayer(Dot11ProbeResp):
        if packet.type == 0 and packet.subtype == 8:
            bssid = packet[Dot11].addr2
            ssid = packet[Dot11Elt].info.decode().strip()
            stats = packet[Dot11Beacon].network_stats()
            channel = stats.get("channel")
            protocol = stats.get("crypto")
            enc = next(iter(protocol))

            if not ssid.strip():
                ssid = 'N/A'

            try:
                dbm = packet.dBm_AntSignal
            except:
                dbm = 'N/A'

            print_results(bssid, ssid, dbm, channel, enc)


def print_results(bssid, ssid, dbm, channel, enc):
    global mac_set

    if bssid not in mac_set:
        mac_set.add(bssid)
        print("{:<24} {:<35} {:<5} {:<7} {}".format(bssid, ssid, dbm, channel, enc))


def run_app():
    global interface

    description = 'Access Point scanner for 2.4 GHz range'
    epilog = 'The author of this code take no responsibility for your use or misuse'
    parser = argparse.ArgumentParser(prog='AccessPointScan.py', description=description, epilog=epilog)
    parser.add_argument('interface', help='your interface in monitor mode')
    parser.add_argument('-a', '--all', help='scan on all 14 channels', default=False, action='store_true')
    parser.add_argument('-c', '--channel', help='scan on specific channel (min 1/max 14)', default=6, type=int)
    args = parser.parse_args()

    if len(args.interface.strip()) < 1:
        print('You did not provide any interface?')
        exit(1)
    else:
        interface = args.interface

    if not args.all and (args.channel < 1 or args.channel > 14):
        print('You will scan on channel {}?'.format(args.channel))
        exit(1)

    if not args.all and args.channel in range(1, 14):
        print("Set channel to {} on interface {}".format(args.channel, interface))

        set_specific_channel(args.channel)

    if args.all:
        channel_changer = Thread(target=change_channel)
        channel_changer.daemon = True
        channel_changer.start()

    print("\nStart scan for beacons and probe responses - to stop press [ctrl] + [c]")
    print("\n{:<24} {:<35} {:<5} {:<7} {}".format("BSSID", "SSID", "dbm", "CH", "ENC"))
    print("-" * 85)

    sniff(prn=evaluate_ap_packet, iface=interface)


if __name__ == "__main__":
    interface = None
    mac_set = set()
    signal.signal(signal.SIGINT, keyboard_interrupt_handler)
    run_app()
