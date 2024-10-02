from server.udp import UDPServer
from decoder.process_query import *
from decoder.fetch_data import *
from generator.generate import *

def recv(q):
    query = DNSQuery(q)
    #query.query_info()
    data = DNSResult(q)
    data_decoded = DNSQuery(data.answer)
    data_decoded.query_info()


def main():
    # config = {
    #     "host": "127.0.0.1",
    #     "port": 530,
    #     "type": "udp"
    # }
    # server = UDPServer(config)
    # for q in server.run():
    #     recv(q)
    data = DNSGenerator("hust.edu.cn", 16)
    recv(data.query)

        

if __name__ == "__main__":
    main()
