from random import randint

class DNSGenerator:
    def __init__(self, domain, type, recursion_desired=True):
        self.domain = domain
        self.type = type
        self.rec = recursion_desired
        self.generate()

    def encode_data(self, data):
        encoded = ""
        for i in data:
            encoded += hex(ord(i))[2:]
        return encoded

    def generate(self):
        query = b""
        self.id = hex(randint(0, 65535))[2:]
        query += bytes.fromhex(self.id)
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
        self.query = query
