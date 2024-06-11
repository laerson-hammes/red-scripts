from benedict import benedict

from colorama import Fore
from colorama import init

from powershell import PowerShell
from macaddress import MACAddress
from devices import ScanNetwork

from customtypes import IPv4DefaultGateway
from customtypes import IPv4Address

import argparse
import asyncio


class ArgParser:

    def __init__(self, /) -> None:
        self.parser = argparse.ArgumentParser()

    def get_arguments(self, /) -> argparse.Namespace:
        """
        This function get command line arguments
        :return target and gateway
        """
        self.parser.add_argument('-ti', '--target-ip', dest='target', help='IPv4 Address of victim / target machine')
        self.parser.add_argument('-gi', '--gateway-ip', dest='gateway', help='Default gateway / router IP')
        return self.parser.parse_args()

    def _target_handler(self, default_gateway: IPv4DefaultGateway, **kwargs) -> IPv4Address:
        '''
        args:
            default_gateway:
                IPv4DefaultGateway -> router ip, you can find it underneath the router or typing ipconfig on Windows or ifconfig on Linux...
            kwargs:
                system: str, -> You can specify the system equal 'Windows' to ping subnet. Its an other way, more slowly, but, works either...
        return:
            Return an device address (IPv4Address)
        '''
        if str(kwargs.get('system', None)).lower() == 'windows':
            devices_address: dict[str, dict] = asyncio.run(
                ScanNetwork.ping_subnet(default_gateway)
            )

            if len(devices_address) == 0:
                print(f'{Fore.RED}[-] NO DEVICES FOUND CONNECTED ON NETWORK...')
                exit()

            address_info: benedict = MACAddress.get_many(**devices_address)

            device: benedict = ScanNetwork.show(**address_info)
            return device.address

        address_info: benedict = ScanNetwork.scan(default_gateway)
        if len(address_info.keys()) == 0:
            print(f'{Fore.RED}[-] NO DEVICES FOUND CONNECTED ON NETWORK...')
            exit()

        device: benedict = ScanNetwork.show(**address_info)
        return device.address

    def _gateway_handler(self, system: str, /) -> IPv4DefaultGateway:
        if system == 'windows':
            return PowerShell.run(
                'Get-NetIPConfiguration | Foreach IPv4DefaultGateway | Select-Object -Property NextHop | Format-List'
            ).strip().split(' : ')[1]

        return input(f"{Fore.GREEN}[+] SPECIFY THE DEFAULT GATEWAY, SOMETHING LIKE 192.168.1.xxx: ")

    def handler(self, system: str, /) -> benedict:
        """
        This function is responsible for checking the command line arguments
        """
        arguments: argparse.Namespace = self.get_arguments()

        if not arguments.gateway:
            arguments.gateway = self._gateway_handler(system)

        if not arguments.target:
            arguments.target = self._target_handler(arguments.gateway)

        return benedict({
            'gateway': arguments.gateway,
            'target': arguments.target
        })


if __name__ != '__main__':
    init(autoreset=True)
