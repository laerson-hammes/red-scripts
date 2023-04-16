import scapy.all as scapy  # type: ignore
import re
import argparse
from colorama import (  # type: ignore
    Fore,
    init
)


class LanScan(object):
    def __init__(self, ip_add: str, /) -> None:
        self.ip_add: str = ip_add
        self.pattern: re.Pattern = re.compile("^(?:[0-9]{1,3}\.){3}[0-9]{1,3}/[0-9]*$")

    def verify_ip_address(self, ip_add: str, /) -> bool:
        return bool(self.pattern.search(ip_add))

    def scan(self, /) -> None:
        if self.verify_ip_address(self.ip_add):
            print(self.ip_add)
            scapy.arping(self.ip_add)
        else:
            print(f"{Fore.RED}[-] INVALID IP ADDRESS AND RANGE...")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-ipr",
        dest="ipr",
        type=str,
        help="Enter the ip address and range that you want to send the ARP request to (ex 192.168.1.0/24)"
    )
    options: argparse.Namespace = parser.parse_args()
    if not options.ipr:
        options.ipr = str(input(f"{Fore.GREEN}[+] ENTER THE IP ADDRESS AND RANGE (EX 192.168.1.0/24): "))
    s = LanScan(str(options.ipr))
    s.scan()


if __name__ == "__main__":
    init(autoreset=True)
    main()
