from random import randint

class DNSGenerator:
    def __init__(self, domain, typ, recursion_desired=True, flag=None, protocol="udp"):
        self.domain = domain
        self.type = typ
        self.rec = recursion_desired
        self.flag = flag
        self.protocol = protocol
        self.generate()

    def encode_data(self, data):
        encoded = ""
        for i in data:
            encoded += hex(ord(i))[2:]
        return encoded

    def generate(self):
        query = b""
        self.id = randint(0, 65535)
        query += bytes.fromhex(f"{self.id:0{4}x}".format())
        self.id = f"{self.id:0{4}x}".format()
        flags = ""
        if self.flag:
            flags += self.flag
        else:
            if self.rec:
                flags = "0120"
            else:
                flags = "0020"
        query += bytes.fromhex(flags)
        query += bytes.fromhex("0001000000000000")
        domain = self.domain.split(".")
        for i in domain:
            query += bytes([len(i)]) + i.encode()
        query += b"\x00" # end of domain
        query += bytes.fromhex(f'{self.type:0{4}x}'.format())  # type
        query += b"\x00\x01"
        if self.protocol == "tcp":
            length = len(query)
            query = bytes([length >> 8, length & 0xFF]) + query
        self.query = query
