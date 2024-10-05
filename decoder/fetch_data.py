from client.udp import UDPClient
from client.tcp import TCPClient

class DNSResult():

    def __init__(self, query, addr="8.8.8.8", port=53, protocol="udp"):
        self.addr = addr
        self.query_raw = query
        self.port = port
        self.protocol = protocol
        self.forward_request()

    def forward_request(self):
        if self.protocol == "udp":
            client = UDPClient(addr=self.addr, port=self.port)
            client.send(self.query_raw)
        elif self.protocol == "tcp":
            client = TCPClient(addr=self.addr, port=self.port)
            length = len(self.query_raw).to_bytes(2, byteorder="big")
            client.send(length + self.query_raw)
        self.status, self.answer = client.status, client.resp
