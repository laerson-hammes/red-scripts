from benedict import benedict

from customtypes import IPv4Address
from customtypes import MACAddr

import scapy.all as scapy


class MACAddress:

    BROADCAST: str = 'ff:ff:ff:ff:ff:ff'

    @classmethod
    def get(cls, address: IPv4Address, /) -> MACAddr:
        arp_request = scapy.ARP(pdst=address)
        broadcast = scapy.Ether(dst=MACAddress.BROADCAST)
        arp_request_broadcast = broadcast/arp_request

        answered_list = scapy.srp(
            arp_request_broadcast,
            timeout=1,
            verbose=False
        )[0]

        try:
            return answered_list[0][1].hwsrc
        except:
            pass

    @classmethod
    def get_many(cls, **devices: dict[str, dict]) -> benedict:
        for key, device in devices.items():
            devices[key].update({
                'mac': MACAddress.get(device.get('address'))
            })

        return benedict(devices)
