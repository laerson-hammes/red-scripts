from abc import abstractmethod
from abc import ABCMeta

from colorama import Fore
from colorama import init


class System(ABCMeta):

    @abstractmethod
    def get_interface():
        ...

    @abstractmethod
    def run_sniffer():
        ...


def system_other_than_error() -> None:
    print(f'{Fore.RED}[-] OPERATING SYSTEM OTHER THAN LINUX OR WINDOWS...')
    exit()


if __name__ != '__main__':
    init(autoreset=True)
