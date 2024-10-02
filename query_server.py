from decoder.fetch_data import *
from decoder.process_query import *
from generator.generate import *
from cache import *
from server.udp import UDPServer
from client.udp import UDPClient
import argparse

argp = argparse.ArgumentParser()
argp.add_argument(
    "--port",
    "-p",
    default=53,
    help="Listen port",
    type=int,
)
argp.add_argument(
    "--recursion",
    "-r",
    default=True,
    help="Recursion supported",
    choices=[True, False],
)
argp.add_argument(
    "--listen",
    "-l",
    default='127.0.0.1',
    help="Listen address",
)
argp.add_argument(
    "--cache",
    "-c",
    default=True,
    help="Cache responses",
    choices=[True, False],
)

def main():
    args = argp.parse_args()
    server = UDPServer({"host": args.listen, "port": args.port})
    cache = Cache()
    for q, client in server.run():
        data = DNSQuery(q)
        if (not args.recursion) and (data.query["flags"]["rd"]):
            ret_raw = DNSGenerator(
                data.query["domain"], data.query["type"], args.recursion, "8100"
            )
            ret = ret_raw.query
        else:
            query = DNSQuery(q)
            if args.cache:
                cached = cache.get((query.query['queries'][0]["name"], query.query['queries'][0]["type"]))
                if cached:
                    ret = bytes.fromhex(data.query['id'])+cached
                else:
                    ret_raw = DNSResult(q)
                    if ret_raw.status == -1:
                        print(f"Error: Socket error {ret_raw.answer}")
                        continue
                    ret = ret_raw.answer
                    ttl = int(1e9)
                    query_ans = DNSQuery(ret).query
                    for t in query_ans['answers']:
                        ttl = min(t['ttl'], ttl)
                    cache.set(
                        (
                            query_ans["queries"][0]["name"],
                            query_ans["queries"][0]["type"],
                        ),
                        ret[2:],
                        ttl,
                    )
            else:
                ret_raw = DNSResult(q)
                if ret_raw.status == -1:
                    print(f"Error: Socket error {ret_raw.answer}")
                    continue
                ret = ret_raw.answer
        server.sock.sendto(ret, client)

if __name__ == "__main__":
    main()
