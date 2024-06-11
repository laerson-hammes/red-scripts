from colorama import Fore
from colorama import init

import subprocess


class PowerShell:

    __DECODE: str = 'cp850'

    @classmethod
    def run(cls, command: str, *, print_command = True) -> str:
        if print_command:
            print(f'{Fore.GREEN}[+] WAITING FOR: ({command})...')

        return subprocess.run([
            "powershell",
            "-Command",
            command
        ], capture_output=True).stdout.decode(PowerShell.__DECODE)


if __name__ != '__main__':
    init(autoreset=True)
