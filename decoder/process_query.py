"""Decodes DNS query packets and prints the information in a human-readable format."""
import bitarray


class DNSQuery:
    """Decodes DNS query packets and prints the information in a human-readable format."""
    def __init__(self, q, protocol="udp"):
        self.query_raw = q
        self.protocol = protocol
        self.cur = 24
        self.query = self.decode_query()

    def is_ptr(self, data):
        """Check if the data is a pointer."""
        ptr = bitarray.bitarray()
        ptr.frombytes(bytes.fromhex(data))
        if ptr[0] == 1 and ptr[1] == 1:
            offset = int(ptr[2:].to01(), 2)*2
            return True, offset
        return False, 0
    def decode_data_offset(self, query, offset):
        """Decode data starting from offset."""
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
            while length > 0:
                offset += 2
                data += chr(int(query[offset : offset + 2], 16))
                length -= 1
            offset+=2
            data += "."
        return data
    def decode_data(self, query):
        """Decode data from the cursor."""
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
            while length > 0:
                self.cur += 2
                data += chr(int(query[self.cur : self.cur + 2], 16))
                length -= 1
            self.cur+=2
            data += "."
        return data
    def decode_query(self):
        """Decode the query."""
        query = self.query_raw.hex()
        ret = {}
        if self.protocol == "tcp":
            ret["length"] = int(query[:4], 16)
            query = query[4:]
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
        for _ in range(ret["qdcount"]):
            qname = self.decode_data(query)
            typ = int(query[self.cur + 2 : self.cur + 6], 16)
            cls = int(query[self.cur + 6 : self.cur + 10], 16)
            ret["queries"].append({"name": qname, "type": typ, "class": cls})
            self.cur += 10
        ret["answers"] = []
        for _ in range(ret["ancount"]):
            ptr, offset = self.is_ptr(query[self.cur : self.cur + 4])
            if ptr:
                self.cur += 4
                qname = self.decode_data_offset(query, offset)
            else:
                qname = self.decode_data(query)
                self.cur += 2
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
                for __ in range(rdlength):
                    rdata += str(int(query[self.cur : self.cur + 2], 16))+"."
                    self.cur += 2
                ret["answers"].append(
                    {
                        "name": qname,
                        "type": typ,
                        "class": cls,
                        "ttl": ttl,
                        "rdlength": rdlength,
                        "rdata": rdata[:-1],
                        "data": rdata[:-1],
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
                        "data": ns
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
                        "data": str(pref) + " " + exchange,
                    }
                )
            elif typ == 28: # AAAA
                short = False
                rdata = ""
                rdata_orig = ""
                for __ in range(8):
                    rdata_orig += query[self.cur : self.cur + 4] + ":"
                    chunk = query[self.cur : self.cur + 4]
                    if chunk == "0000":
                        if not short:
                            short = True
                    else:
                        if short:
                            rdata += ':'
                            short = False
                        for j in range(4):
                            if chunk[j] != "0":
                                rdata += chunk[j:]
                                break
                        rdata += ":"
                    self.cur += 4
                ret["answers"].append(
                    {
                        "name": qname,
                        "type": typ,
                        "class": cls,
                        "ttl": ttl,
                        "rdlength": rdlength,
                        "rdata_orig": rdata_orig[:-1],
                        "rdata": rdata[:-1],
                        "data": rdata[:-1],
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
                        "data": " ".join(txt),
                    })
            elif typ == 6: # CNAME
                cname = self.decode_data(query)
                ret["answers"].append(
                    {
                        "name": qname,
                        "type": typ,
                        "class": cls,
                        "ttl": ttl,
                        "rdlength": rdlength,
                        "cname": cname,
                        "data": cname
                    }
                )
            else:
                ret["answers"].append(
                    {
                        "name": qname,
                        "type": typ,
                        "class": cls,
                        "ttl": ttl,
                        "rdlength": rdlength,
                        "raw": query[self.cur : self.cur + rdlength*2],
                    })
        ret["authorities"] = []
        for _ in range(ret["nscount"]):
            ptr, offset = self.is_ptr(query[self.cur : self.cur + 4])
            if ptr:
                self.cur += 4
                name = self.decode_data_offset(query, offset)
            else:
                name = self.decode_data(query)
                self.cur += 2
            typ = int(query[self.cur : self.cur + 4], 16)
            self.cur += 4
            cls = int(query[self.cur : self.cur + 4], 16)
            self.cur += 4
            ttl = int(query[self.cur : self.cur + 8], 16)
            self.cur += 8
            rdlength = int(query[self.cur : self.cur + 4], 16)
            self.cur += 4
            if typ == 2: # NS
                ns = self.decode_data(query)
                ret["authorities"].append(
                    {
                        "name": name,
                        "type": typ,
                        "class": cls,
                        "ttl": ttl,
                        "rdlength": rdlength,
                        "ns": ns,
                        "data": ns
                    }
                )
            elif typ == 6:  # SOA
                mname = self.decode_data(query)
                ret["authorities"].append(
                    {
                        "name": qname,
                        "type": typ,
                        "class": cls,
                        "ttl": ttl,
                        "rdlength": rdlength,
                        "mname": mname,
                        "data": mname
                    }
                )
        return ret

    def query_info(self):
        """Print the query information."""
        typ = {
            1: "A",
            2: "NS",
            5: "CNAME",
            6: "SOA",
            15: "MX",
            16: "TXT",
            28: "AAAA",
        }
        cls = {1: "IN", 3: "CH", 4: "HS", 255: "ANY"}
        qid = self.query["id"]
        for i in self.query["queries"]:
            print(f"Query: ID {qid} Protocol {self.protocol} {i['name'][:-1]} {typ[i['type']]} {cls[i['class']]}")
        if self.query["flags"]["rcode"] != '0000':
            err_map = {
                "0001": "Format error",
                "0010": "Server failure",
                "0011": "No such domain",
                "0100": "Not implemented",
                "0101": "Refused",
            }
            print(f"\nError: ID {qid} Protocol {self.protocol} {err_map[self.query['flags']['rcode']]}")
            return
        for i in self.query["answers"]:
            try:
                t = i["type"]
            except ValueError:
                print(f"Error: ID {qid} Protocol {self.protocol} Invalid type {i['type']}")
                continue
            print(
                f"\nAnswer: ID {qid} Protocol {self.protocol} {i['name'][:-1]} {typ[i['type']]}"
            )
            print(f"    TTL: {i['ttl']}")
            if t == 15: # MX
                print(f"    PRIORITY: {i['pref']} EXECHANGE: {i['exchange']}")
            elif t == 1 or i["type"] == 28: # A or AAAA
                print(f"    RDATA: {i['rdata']}")
            elif t == 2: # NS
                print(f"    NS: {i['ns']}")
            elif t == 16: # TXT
                print(f"    TXT: {i['txt']}")
            elif t == 6: # CNAME
                print(f"    CNAME: {i['cname']}")
        for i in self.query["authorities"]:
            print(f"\nAuthority: ID {qid} Protocol {self.protocol} {i['name'][:-1]} {typ[i['type']]}")
            print(f"    TTL: {i['ttl']}")
            if i["type"] == 2:
                print(f"    NS: {i['ns']}")
            elif i["type"] == 6:
                print(f"    MNAME: {i['mname']}")
