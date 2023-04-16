from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from typing import List
from colorama import (  # type: ignore
    Fore,
    init
)
import requests
import argparse
import sys


class FindDashboard(object):

    def __init__(self, hostname: str, wordlist: str, /) -> None:
        self.hostname: str = f"https://{hostname}"
        self.wordlist: Path = Path(wordlist)

    def verify_response(self, word: str, /) -> str:
        url: str = f"{self.hostname}/{word}"
        try:
            result: requests.models.Response = requests.get(url, timeout=5)
            if result.status_code == 200:
                return f"{Fore.GREEN}[+] {result.status_code}: {url}..."
            return f"{Fore.RED}[-] {result.status_code}: {url}..."
        except requests.exceptions.Timeout:
            return f"{Fore.RED}[-] REQUEST TIMED OUT {url}..."

    def read_wordlist(self, /) -> List[str]:
        if self.wordlist.exists() and self.wordlist.is_file():
            words: List[str] = []
            with open(self.wordlist, mode="r") as f:
                words.extend(line.rstrip().replace(".", "") for line in f)
            return words
        else:
            print(f"{Fore.RED}[-] FILE NOT FOUND ERROR...")
            sys.exit(1)

    def run(self, /) -> None:
        print(f"{Fore.GREEN}[+] HOSTNAME {self.hostname}...")
        words: List[str] = self.read_wordlist()
        with ThreadPoolExecutor(len(words)) as executor:
            results = executor.map(self.verify_response, words)
            for row in results:
                print(row)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-hn",
        "--host",
        type=str,
        dest="host",
        help="Enter with the hostname"
    )
    parser.add_argument(
        "-w",
        "--wordlist",
        type=str,
        dest="wordlist",
        help="Enter with the path / filename from your wordlist"
    )
    options: argparse.Namespace = parser.parse_args()
    if not options.host:
        options.host = str(input(f"{Fore.GREEN}[+] HOSTNAME: "))
    if not options.wordlist:
        options.wordlist = str(input(f"{Fore.GREEN}[+] PATH / FILENAME FROM YOUR WORDLIST: "))
    find_dash = FindDashboard(str(options.host), str(options.wordlist))
    find_dash.run()


if __name__ == "__main__":
    init(autoreset=True)
    main()
