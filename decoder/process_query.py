import bitarray


class DNSQuery:
    def __init__(self, q):
        self.query_raw = q
        self.cur = 24
        self.query = self.decode_query()

    def is_ptr(self, hex):
        ptr = bitarray.bitarray()
        ptr.frombytes(bytes.fromhex(hex))
        if ptr[0] == 1 and ptr[1] == 1:
            offset = int(ptr[2:].to01(), 2)*2
            return True, offset
        return False, 0
    def decode_data_offset(self, query, offset):
        data = ""
        while True:
            length = int(query[offset : offset + 2], 16)
            if length == 0:
                break
            ptr, offset_n = self.is_ptr(query[offset : offset + 4])
            if ptr:
                offset += 4
                data += self.decode_data_offset(query, offset_n)
                break
            else:
                while length > 0:
                    offset += 2
                    data += chr(int(query[offset : offset + 2], 16))
                    length -= 1
                offset+=2
                data += "."
        return data
    def decode_data(self, query):
        data = ""
        while True:
            length = int(query[self.cur : self.cur + 2], 16)
            if length == 0:
                break
            ptr, offset = self.is_ptr(query[self.cur : self.cur + 4])
            if ptr:
                self.cur += 4
                data += self.decode_data_offset(query, offset)
                break
            else:
                while length > 0:
                    self.cur += 2
                    data += chr(int(query[self.cur : self.cur + 2], 16))
                    length -= 1
                self.cur+=2
                data += "."
        return data
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
        for i in range(ret["qdcount"]):
            qname = self.decode_data(query)
            typ = int(query[self.cur + 2 : self.cur + 6], 16)
            cls = int(query[self.cur + 6 : self.cur + 10], 16)
            ret["queries"].append({"name": qname, "type": typ, "class": cls})
            self.cur += 10
        ret["answers"] = []
        for i in range(ret["ancount"]):
            ptr, offset = self.is_ptr(query[self.cur : self.cur + 4])
            if ptr:
                self.cur += 4
                qname = self.decode_data_offset(query, offset)
            else:
                qname = self.decode_data(query)
            typ = int(query[self.cur : self.cur + 4], 16)
            self.cur+=4
            cls = int(query[self.cur : self.cur + 4], 16)
            self.cur+=4
            ttl = int(query[self.cur : self.cur + 8], 16)
            self.cur+=8
            rdlength = int(query[self.cur : self.cur + 4], 16)
            self.cur+=4
            if typ == 1: # A
                rdata = ""
                for j in range(rdlength):
                    rdata += str(int(query[self.cur : self.cur + 2], 16))+"."
                    self.cur += 2
                ret["answers"].append(
                    {
                        "name": qname,
                        "type": typ,
                        "class": cls,
                        "ttl": ttl,
                        "rdlength": rdlength,
                        "rdata": rdata,
                    }
                )
            elif typ == 2: # NS
                ns = self.decode_data(query)
                ret["answers"].append(
                    {
                        "name": qname,
                        "type": typ,
                        "class": cls,
                        "ttl": ttl,
                        "rdlength": rdlength,
                        "ns": ns,
                    }
                )
            elif typ == 5: # CNAME
                cname = self.decode_data(query)
                ret["answers"].append(
                    {
                        "name": qname,
                        "type": typ,
                        "class": cls,
                        "ttl": ttl,
                        "rdlength": rdlength,
                        "cname": cname,
                    }
                )
            elif typ == 15: # MX
                pref = int(query[self.cur : self.cur + 4], 16)
                self.cur+=4
                exchange = self.decode_data(query)
                ret["answers"].append(
                    {
                        "name": qname,
                        "type": typ,
                        "class": cls,
                        "ttl": ttl,
                        "rdlength": rdlength,
                        "pref": pref,
                        "exchange": exchange,
                    }
                )
            elif typ == 16: # TXT
                rl = rdlength
                txt = []
                while rl > 0:
                    length = int(query[self.cur : self.cur + 2], 16)
                    self.cur += 2
                    rl -= 1
                    label = ""
                    for j in range(length):
                        label += chr(int(query[self.cur : self.cur + 2], 16))
                        self.cur += 2
                        rl -= 1
                    txt.append(label)
                ret["answers"].append(
                    {
                        "name": qname,
                        "type": typ,
                        "class": cls,
                        "ttl": ttl,
                        "rdlength": rdlength,
                        "txt": txt,
                    })

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
        id = self.query["id"]
        for i in self.query["queries"]:
            print(f"Query: ID {id} {i['name'][:-1]} {typ[i['type']]} {cls[i['class']]}")
        for i in self.query["answers"]:
            print(f"Answer: ID {id} {i['name'][:-1]} {typ[i['type']]}")
            print(f"TTL: {i['ttl']}")
            if i["type"] == 15: # MX
                print(f"{i['pref']} {i['exchange']}")
            elif i["type"] == 1: # A
                print(f"  RDATA: {i['rdata']}")
            elif i["type"] == 5: # CNAME
                print(f"  CNAME: {i['cname']}")
            elif i["type"] == 2: # NS
                print(f"  NS: {i['ns']}")
            elif i["type"] == 16: # TXT
                print(f"  TXT: {i['txt']}")
