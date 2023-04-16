from concurrent.futures import ThreadPoolExecutor
from typing import Tuple
import socket
from colorama import (  # type: ignore
   Fore,
   init
)
import argparse
import sys


DEFAULT_HOSTNAME: str = "127.0.0.1"
DEFAULT_PORT_RANGE: str = "1-65535"


class PortScan(object):

    def __init__(self, hostname: str, port: str, /) -> None:
        self.hostname: str = socket.gethostbyname(hostname)
        self.port: str = port
        self.sock = None

    def check_port_range(self, /) -> Tuple[int, int]:
        if len(self.port.split("-")) == 2:
            start, end = self.port.split("-")
            if int(start) > int(end):
                print(f"{Fore.RED}[-] START ELEMENT OF PORT RANGE MUST BE LESS THAN TO END...")
                sys.exit(1)
            return (int(start), int(end))
        return (-1, int(self.port))

    def check_port(self, port: int, /) -> str:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(3)
            try:
                sock.connect((self.hostname, port))
                return f"{Fore.GREEN}[+] {port} OPEN"
            except Exception:
                return f"{Fore.RED}[-] {port} CLOSED"

    def scan(self, /) -> None:
        start, end = self.check_port_range()
        print(f"{Fore.GREEN}[+] SCANNING {self.hostname}...")
        if start != -1:
            ports = range(start, end + 1)
            with ThreadPoolExecutor(len(ports)) as executor:
                results = executor.map(self.check_port, ports)
                for row in results:
                    if row.endswith("OPEN"):
                        print(row)
        else:
            print(self.check_port(int(self.port)))


def main():
    parser: argparse.ArgumentParser = argparse.ArgumentParser()
    parser.add_argument(
        "--host",
        dest="host",
        type=str,
        default=DEFAULT_HOSTNAME,
        help="Enter with the ip address"
    )
    parser.add_argument(
        "--port",
        dest="port",
        type=str,
        default=DEFAULT_PORT_RANGE,
        help="Port to scan. Default is '1-65535'"
    )
    options: argparse.Namespace = parser.parse_args()
    s: PortScan = PortScan(options.host, options.port)
    s.scan()


if __name__ == "__main__":
    init(autoreset=True)
    main()
