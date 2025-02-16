"""Server to accept, decode and forward DNS queries."""
import argparse

from cache import Cache
from decoder.fetch_data import DNSResult
from decoder.process_query import DNSQuery
from generator.generate import DNSGenerator
from server.tcp import TCPServer
from server.udp import UDPServer

argp = argparse.ArgumentParser()
argp.add_argument(
    "--port",
    "-p",
    default=53,
    help="Listen port",
    type=int,
)
argp.add_argument(
    "--no-recursion",
    "-nr",
    dest="recursion",
    action="store_false",
    help="Disable iterative mode",
)
argp.add_argument(
    "--listen",
    "-l",
    default="127.0.0.1",
    help="Listen address",
)
argp.add_argument(
    "--cache",
    "-c",
    action="store_true",
    help="Cache responses",
)
argp.add_argument(
    "--cache-file",
    "-f",
    help="Cache file",
)
argp.add_argument(
    "--tcp",
    "-t",
    action="store_true",
    help="Allow TCP",
)


def main():
    """Main function."""
    args = argp.parse_args()
    if args.tcp:
        server = TCPServer({"host": args.listen, "port": args.port, "backlog": 5})
        protocol = "tcp"
    else:
        server = UDPServer({"host": args.listen, "port": args.port})
        protocol = "udp"
    cache = Cache()
    if args.cache and args.cache_file:
        try:
            cache.load(args.cache_file)
        except FileNotFoundError:
            print(f"Cache file {args.cache_file} not found, will be created")
    try:
        for q, client in server.run():
            data = DNSQuery(q, protocol)
            if (not args.recursion) and (data.query["flags"]["rd"]):
                ret_raw = DNSGenerator(
                    data.query["name"],
                    data.query["type"],
                    args.recursion,
                    "8100",
                    protocol,
                )
                ret = ret_raw.query
            else:
                if args.cache:
                    cached = cache.get(
                        (
                            data.query["queries"][0]["name"],
                            data.query["queries"][0]["type"],
                        )
                    )
                    if cached:
                        ret = bytes.fromhex(data.query["id"]) + cached
                        if protocol == "tcp":
                            ret = len(ret).to_bytes(2, byteorder="big") + ret
                    else:
                        if protocol == "tcp":
                            ret_raw = DNSResult(q[2:], protocol=protocol)
                        else:
                            ret_raw = DNSResult(q, protocol=protocol)
                        if ret_raw.status == -1:
                            print(f"Error: Socket error {ret_raw.answer}")
                            continue
                        ret = ret_raw.answer
                        ttl = int(1e9)
                        query_ans = DNSQuery(ret, protocol=protocol).query
                        for t in query_ans["answers"]:
                            ttl = min(t["ttl"], ttl)
                        if protocol == "tcp":
                            ret_save = ret[4:]
                        else:
                            ret_save = ret[2:]
                        cache.set(
                            (
                                query_ans["queries"][0]["name"],
                                query_ans["queries"][0]["type"],
                            ),
                            ret_save,
                            ttl,
                            0,
                        )
                else:
                    ret_raw = DNSResult(q, protocol=protocol)
                    if ret_raw.status == -1:
                        print(f"Error: Socket error {ret_raw.answer}")
                        continue
                    ret = ret_raw.answer
            if protocol == "tcp":
                client.send(ret)
            else:
                server.sock.sendto(ret, client)
    except KeyboardInterrupt:
        print("Exiting")
    if args.cache and args.cache_file:
        cache.save(args.cache_file)
    server.sock.close()


if __name__ == "__main__":
    main()
