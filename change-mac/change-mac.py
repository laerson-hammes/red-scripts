from colorama import (  # type: ignore
    Fore,
    init
)
import subprocess
import argparse
import platform
import random
import re

# Restart-NetAdapter

init(autoreset=True)


class MACAddressError(Exception):

    def __init__(self, message: str) -> None:
        super(MACAddressError, self).__init__(message)


class Windows:

    def change(self, new_mac: str, interface=None, /) -> None:
        if not (net_adapter := self.get_current_mac()):
            raise MACAddressError(f"{Fore.RED}[-] COULD NOT READ MAC ADDRESS...")

        print(f"{Fore.GREEN}[+] CURRENT MAC {net_adapter['mac']}...")
        print(f"{Fore.GREEN}[+] CHANGING MAC ADDRESS FOR {net_adapter['name']} TO {new_mac.replace(':', '-')}")
        subprocess.run([
            "powershell",
            "-Command",
            f"Set-NetAdapter -Name {net_adapter['name']} -MacAddress '{new_mac.replace(':', '-')}'"
        ])

        if current := self.get_current_mac():
            if net_adapter['mac'] != current["mac"]:
                print(f"{Fore.GREEN}[+] MAC ADDRESS WAS SUCCESSFULLY CHANGED...")
            else:
                print(f"{Fore.RED}[-] MAC ADDRESS DID NOT GET CHANGED...")

    def get_current_mac(self, /) -> dict[str, str] | None:
        try:
            get_netadapter = subprocess.run(
                [
                    "powershell",
                    "-Command",
                    "Get-NetAdapter -Physical | Format-List -Property 'MacAddress', 'Name'"
                ],
                capture_output=True
            ).stdout.decode("cp850").rsplit()
            return {
                "name": get_netadapter[5],
                "mac": get_netadapter[2]
            }
        except Exception:
            return None


class Linux:

    def change(self, new_mac: str, interface: str, /) -> None:
        if not (current_mac := self.get_current_mac(interface)):
            raise MACAddressError(f"{Fore.RED}[-] COULD NOT READ MAC ADDRESS...")

        print(f"{Fore.GREEN}[+] CURRENT MAC {current_mac}...")
        print(f"{Fore.GREEN}[+] CHANGING MAC ADDRESS FOR {interface} TO {new_mac}")
        subprocess.call(["ifconfig", interface, "down"])
        subprocess.call(["ifconfig", interface, "hw", "ether", new_mac])
        subprocess.call(["ifconfig", interface, "up"])

        if new_mac_address := self.get_current_mac(interface):
            if current_mac != new_mac_address:
                print(f"{Fore.GREEN}[+] MAC ADDRESS WAS SUCCESSFULLY CHANGED...")
            else:
                print(f"{Fore.RED}[-] MAC ADDRESS DID NOT GET CHANGED...")

    def get_current_mac(self, interface: str, /) -> str | None:
        ifconfig = subprocess.check_output(["ifconfig", interface]).decode("ASCII")
        try:
            mac = re.compile(r"([A-Za-z0-9]{2}[:-]){5}([A-Za-z0-9]{2})")
            return mac.findall(ifconfig)[1]
        except Exception:
            return None


class MACAddress:

    def __init__(self, interface: str | None, os, /) -> None:
        self.interface = interface
        self.os = os

    def change(self, /) -> None:
        self.os.change(self.generate(), self.interface)

    @staticmethod
    def generate() -> str:
        return ":".join(
            [f'0{hex(random.randint(0, 256))[2:]}'[-2:].upper() for _ in range(6)]
        )


class ArgParser:

    def __init__(self, /) -> None:
        self.parser = argparse.ArgumentParser()

    def get_arguments(self, /) -> argparse.Namespace:
        """
        This function get command line arguments
        :return interface
        """
        self.parser.add_argument(
            "-i",
            "--interface",
            dest="interface",
            help="Interface to change its MAC Address..."
        )
        return self.parser.parse_args()

    def main(self, /) -> str:
        """
        This function is responsible for checking the command line arguments
        """
        arguments: argparse.Namespace = self.get_arguments()

        if not arguments.interface:
            arguments.interface = input(f"{Fore.GREEN}[+] SPECIFY AN INTERFACE: ")
        return arguments.interface


os = {
    "Windows": Windows(),
    "Linux": Linux(),
}


if __name__ == "__main__":
    args = ArgParser().main() if (system := platform.system()) == "Linux" else None
    mac = MACAddress(args, os.get(system))
    mac.change()
