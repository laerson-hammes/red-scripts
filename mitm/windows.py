from powershell import PowerShell
from system import System
from pathlib import Path


class Windows(System):

    @classmethod
    def get_interface(cls, /) -> str:
        return PowerShell.run(
            'Get-NetAdapter -Physical | Select-Object Name | Format-List',
            print_command=False
        ).strip().split(' : ')[1]

    @classmethod
    def run_sniffer(cls, /) -> None:
        PowerShell.run(
            f'Start-Process -FilePath "powershell" -WorkingDirectory "{str(Path(__file__.rsplit('\\', maxsplit=1)[0]))}" -ArgumentList "py sniffer.py"',
            print_command=False
        )
