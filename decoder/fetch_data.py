from client.udp import UDPClient
from .process_query import DNSQuery

class DNSResult():

    def __init__(self, query, addr="8.8.8.8"):
        self.addr = addr
        self.query_raw = query
        self.answer = self.forward_request()

    def forward_request(self):
        client = UDPClient(addr=self.addr, port=53)
        client.send(self.query_raw)
        return client.resp

    def __str__(self):
        return f"{self.answer}"
