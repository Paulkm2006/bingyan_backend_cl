import bitarray


class DNSQuery:
    def __init__(self, q):
        self.query_raw = q
        self.query = self.decode_query()

    def decode_query(self):
        query = self.query_raw.hex()
        ret = {}
        ret["id"] = query[:4]
        flags = bitarray.bitarray()
        flags.frombytes(bytes.fromhex(query[4:8]))
        ret["flags"] = {
            "qr": flags[0],
            "opcode": flags[1:5].to01(),
            "aa": flags[5],
            "tc": flags[6],
            "rd": flags[7],
            "ra": flags[8],
            "z": flags[9:12].to01(),
            "rcode": flags[12:16].to01(),
        }
        ret["qdcount"] = int(query[8:12], 16)
        ret["ancount"] = int(query[12:16], 16)
        ret["nscount"] = int(query[16:20], 16)
        ret["arcount"] = int(query[20:24], 16)
        ret["queries"] = []
        cur = 22
        for i in range(ret["qdcount"]):
            qname = ""
            while True:
                cur += 2
                length = int(query[cur : cur + 2], 16)
                if length == 0:
                    break
                else:
                    while length > 0:
                        cur += 2
                        qname += chr(int(query[cur : cur + 2], 16))
                        length -= 1
                    qname += "."
            typ = int(query[cur + 2 : cur + 6], 16)
            cls = int(query[cur + 6 : cur + 10], 16)
            ret["queries"].append({"name": qname, "type": typ, "class": cls})
        ret["answers"] = []
        cur+=8
        for i in range(ret["ancount"]):
            cur += 2
            ptr = bitarray.bitarray()
            ptr.frombytes(bytes.fromhex(query[cur : cur + 4]))
            offset = int(ptr[2:].to01(), 2)*2 -2
            qname = ""
            while True:
                offset += 2
                length = int(query[offset : offset + 2], 16)
                if length == 0:
                    break
                else:
                    while length > 0:
                        offset += 2
                        qname += chr(int(query[offset : offset + 2], 16))
                        length -= 1
                    qname += "."
            cur+=4
            typ = int(query[cur : cur + 4], 16)
            cur+=4
            cls = int(query[cur : cur + 4], 16)
            cur+=4
            ttl = int(query[cur : cur + 8], 16)
            cur+=8
            rdlength = int(query[cur : cur + 4], 16)
            cur+=4
            rdata = ""
            for j in range(rdlength):
                rdata += str(int(query[cur : cur + 2], 16))+"."
                cur += 2
            ret["answers"].append({"name": qname, "type": typ, "class": cls, "ttl": ttl, "rdlength": rdlength, "rdata": rdata})
        return ret

    def query_info(self):
        typ = {
            1: "A",
            2: "NS",
            5: "CNAME",
            6: "SOA",
            12: "PTR",
            15: "MX",
            16: "TXT",
            28: "AAAA",
            33: "SRV",
            252: "AXFR",
            255: "ANY",
        }
        cls = {1: "IN", 3: "CH", 4: "HS", 255: "ANY"}
        for i in self.query["queries"]:
            print(f"Query: {i['name'][:-1]} {typ[i['type']]} {cls[i['class']]}")
        for i in self.query["answers"]:
            print(f"Answer: {i['name'][:-1]} {typ[i['type']]}")
            print(f"  TTL: {i['ttl']}")
            print(f"  RDATA: {i['rdata']}")
