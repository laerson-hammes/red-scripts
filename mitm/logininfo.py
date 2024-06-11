from scapy.layers.ipsec import Raw

from scapy.layers.l2 import Ether


class LoginInfo:

    '''
    You can add more items here, make a web crawler maybe, and get names from login pages, ...
    '''
    LOGIN: list[str] = [
        'username',
        'user',
        'login',
        'password',
        'pass',
        'email',
        'cpf',
        'Cpf',
        'txtLogin',
        'txtSenha',
        'senha'
    ]

    @staticmethod
    def get_info(packet: Ether) -> Raw.load:
        if not packet.haslayer(Raw):
            return

        load = str(packet[Raw].load)
        for keyword in LoginInfo.LOGIN:
            if keyword in load:
                return load
