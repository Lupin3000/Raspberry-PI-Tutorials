#!/usr/bin/env python3

import argparse
import datetime
import signal
from os import system
from scapy.layers.dot11 import Dot11ProbeReq, Dot11Elt, RadioTap, sniff
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


def evaluate_sta_packet(packet):
    global filter_results
    print_out = True

    if packet.haslayer(Dot11ProbeReq) and packet.haslayer(Dot11Elt):
        if packet.type == 0 and packet.subtype == 4:
            mac = packet.addr2
            ssid = packet[Dot11Elt].info.decode().strip()
            date_time = datetime.datetime.now()
            rssi = packet.dBm_AntSignal

            if filter_results and not ssid:
                print_out = False

            if not ssid:
                ssid = 'N/A'

            if print_out:
                print_results(mac, ssid, date_time, rssi)


def print_results(mac, ssid, date_time, rssi):
    global mac_set

    if mac not in mac_set:
        mac_set.add(mac)
        print("{:<22} {:<20} {:<5} {}".format(date_time.strftime("%Y %b %d %H:%M:%S"), mac, rssi, ssid))


def run_app():
    global interface
    global filter_results

    description = 'Station scanner for 2.4 GHz range'
    epilog = 'The author of this code take no responsibility for your use or misuse'
    parser = argparse.ArgumentParser(prog='StationScan.py', description=description, epilog=epilog)
    parser.add_argument('interface', help='your interface in monitor mode')
    parser.add_argument('--filter', help='do not show hidden SSID searches', default=False, action='store_true')
    args = parser.parse_args()

    if len(args.interface.strip()) < 1:
        print('You did not provide any interface?')
        exit(1)
    else:
        interface = args.interface

    if args.filter:
        filter_results = True
    else:
        filter_results = False

    channel_changer = Thread(target=change_channel)
    channel_changer.daemon = True
    channel_changer.start()

    print("\nStart scan for probe requests - to stop press [ctrl] + [c]")
    print("\n{:<22} {:<20} {:<5} {}".format("Time", "MAC Address", "dBm", "SSID"))
    print("-" * 85)

    sniff(prn=evaluate_sta_packet, iface=interface)


if __name__ == "__main__":
    interface = filter_results = None
    mac_set = set()
    signal.signal(signal.SIGINT, keyboard_interrupt_handler)
    run_app()
