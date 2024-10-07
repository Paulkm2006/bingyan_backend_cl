"""Receive DNS query and decode it."""
from decoder.process_query import DNSQuery
from decoder.fetch_data import DNSResult
from generator.generate import DNSGenerator

def recv(q):
    """Receive DNS query"""
    # query = DNSQuery(q)
    # query.query_info()
    data = DNSResult(q, protocol="tcp", addr="223.5.5.5")
    data_decoded = DNSQuery(data.answer)
    data_decoded.query_info()


def main():
    """Main function."""
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
