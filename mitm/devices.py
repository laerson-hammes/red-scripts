from benedict import benedict

from typing import Optional

from colorama import Fore
from colorama import init

import scapy.all as scapy

from customtypes import IPv4DefaultGateway

from powershell import PowerShell

import asyncio


class ScanNetwork:

    BROADCAST: str = 'ff:ff:ff:ff:ff:ff'
    MAX_SUBNETS: int = 254
    devices: dict = dict()

    @classmethod
    def _format_address(cls, splited_gateway: list[str], number: int) -> str:
        splited_gateway[-1] = str(number)
        return '.'.join(splited_gateway)

    @classmethod
    async def _ping(cls, address: str) -> str:
        return PowerShell.run(
            f'ping.exe -n 1 -l 0 -f -i 255 -w 1 -4 {address}',
            print_command=False
        )

    @classmethod
    async def ping_subnet(cls, default_gateway: IPv4DefaultGateway) -> dict[str, dict]:
        '''
        IPv4DefaultGateway -> 192.168.xyz.
        '''
        print(f'{Fore.GREEN}[+] SEARCHING FOR DEVICES ON NETWORK...')

        splited_gateway: list[str] = default_gateway.split('.')

        for device in range(int(splited_gateway[-1]) + 1, ScanNetwork.MAX_SUBNETS + 1):
            address: str = ScanNetwork._format_address(splited_gateway, device)

            task = asyncio.create_task(ScanNetwork._ping(address))
            await task

            if (result := task.result()) and 'Received = 1' in result:
                ScanNetwork.devices.update({
                    str(len(ScanNetwork.devices)): {
                        'address': address
                    }
                })

        return ScanNetwork.devices

    @classmethod
    def scan(cls, default_gateway: IPv4DefaultGateway):
        arp_request = scapy.ARP(pdst=f'{default_gateway}/24')
        broadcast = scapy.Ether(dst=ScanNetwork.BROADCAST)
        arp_request_broadcast = broadcast/arp_request
        answered_list = scapy.srp(arp_request_broadcast, timeout=1, verbose=False)[0]

        for element in answered_list:
            ScanNetwork.devices.update({
                str(len(ScanNetwork.devices)): {
                    'address': element[1].psrc,
                    'mac': element[1].hwsrc
                }
            })

        return ScanNetwork.devices

    @classmethod
    def _handle_option(cls, option: str, **devices: dict[str, dict]) -> Optional[benedict]:
        if option not in devices.keys():
            print(f'{Fore.RED}[-] INVALID OPTION...')
            exit()

        return benedict(devices.get(option))

    @classmethod
    def show(cls, **devices: dict[str, dict]) -> Optional[benedict]:
        print(f'{Fore.GREEN}[+] DEVICES FOUND: ')

        for key, device in devices.items():
            print(f'{Fore.GREEN}[+] {key}) ADDRESS: {device.get('address')} | MAC: {device.get('mac')}')

        option: str = input(f'{Fore.GREEN}[+] CHOOSE AN OPTION: ')
        return benedict(
            ScanNetwork._handle_option(option, **devices)
        )


if __name__ != '__main__':
    init(autoreset=True)
