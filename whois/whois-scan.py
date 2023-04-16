from whois import whois  # type: ignore
import argparse
from colorama import (  # type: ignore
   Fore,
   init
)


class WhoisScan(object):
    def __init__(self, domain: str, /, *, cli: bool = True) -> None:
        self.domain: str = domain
        self.cli: bool = cli

    def scan_whois(self, /) -> None:
        if self.cli:
            print(f"{Fore.GREEN}[+] DOMAIN NAME: {self.domain}")
        consult: whois.parser.WhoisBr = whois(str(self.domain))
        print(f"{Fore.GREEN}{consult.text}")
        with open(f"{self.domain}.txt", mode="w", encoding="utf-8", errors="ignore") as f:
            f.write(consult.text)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-d", "--domain",
        dest="domain",
        type=str,
        help="Domain name"
    )
    options: argparse.Namespace = parser.parse_args()
    if not options.domain:
        options.domain = str(input(f"{Fore.GREEN}[+] DOMAIN NAME: "))
        w: WhoisScan = WhoisScan(options.domain, cli=False)
    else:
        w: WhoisScan = WhoisScan(str(options.domain))
    w.scan_whois()


if __name__ == "__main__":
    init(autoreset=True)
    main()
