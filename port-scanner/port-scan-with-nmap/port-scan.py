# https://pypi.org/project/python-nmap/
import nmap
import argparse
from colorama import (  # type: ignore
    Fore,
    init
)


DEFAULT_HOSTNAME = "127.0.0.1"
DEFAULT_PORT_RANGE = "22-40043"


class PortScan(object):

    def __init__(self, hostname: str, portrange: str) -> None:
        self.hostname: str = hostname
        self.portrange: str = portrange
        try:
            self.nm: nmap.PortScanner = nmap.PortScanner()
        except nmap.PortScannerError:
            print(f"{Fore.RED}[-] NMAP IS NOT FOUND IN THE PATH...")

    def scan(self, /) -> None:

        self.nm.scan(self.hostname, self.portrange)

        for host in self.nm.all_hosts():

            print(f"{Fore.GREEN}[+] SCANNING: [\"{host}\"]...")

            if self.nm[host].hostname():
                print(f"{Fore.GREEN}[+] HOSTNAME: {self.nm[host].hostname()}")

            if self.nm[host].state() == "up":
                print(f"{Fore.GREEN}[+] STATE: UP")
            else:
                print(f"{Fore.RED}[+] STATE: DOWN")

            for protocol in self.nm[host].all_protocols():
                print("----------")
                print(f"{Fore.GREEN}[+] Protocol: {protocol}")
                for port in self.nm[host][protocol].keys():
                    if self.nm[host][protocol][port]['state'] == "open":
                        print(f"{Fore.GREEN}[+] PORT OPEN: {port}...")
                    else:
                        print(f"{Fore.RED}[+] PORT OPEN: {port}...")


def main():
    parser: argparse.ArgumentParser = argparse.ArgumentParser()
    parser.add_argument(
        "--host",
        dest="host",
        type=str,
        default=DEFAULT_HOSTNAME,
        help="Hostname / domain for scan."
    )
    parser.add_argument(
        "--port",
        dest="port",
        type=str,
        default=DEFAULT_PORT_RANGE,
        help="Port or port range to scan. Default is '22-40043'"
    )
    options: argparse.Namespace = parser.parse_args()
    s: PortScan = PortScan(options.host, options.port)
    s.scan()


if __name__ == "__main__":
    init(autoreset=True)
    main()
