"""DNS query tool"""

import argparse

from cache import Cache
from decoder.fetch_data import DNSResult
from decoder.process_query import DNSQuery
from generator.generate import DNSGenerator

argp = argparse.ArgumentParser()
argp.add_argument(
    "--type",
    "-t",
    default="A",
    help="Query type",
    choices=["A", "NS", "CNAME", "MX", "AAAA", "TXT"],
)
argp.add_argument(
    "--iterative",
    "-i",
    dest="recursion",
    action="store_false",
    help="Use iterative mode",
)
argp.add_argument("--server", "-s", default="8.8.8.8", help="DNS server")
argp.add_argument("--port", default=53, type=int, help="DNS server port")
argp.add_argument("--protocol", default="udp", help="Protocol", choices=["udp", "tcp"])
argp.add_argument(
    "--no-cache", "-nc", dest="cache", action="store_false", help="Disable cache"
)
argp.add_argument("--cache-file", "-f", default="cache.pickle", help="Cache file")
argp.add_argument(
    "--like", "-l", action="store_true", help="Add query into likes (requires cache)"
)
argp.add_argument(
    "data",
    help="Domain to query/command(history, like, rank, clear)",
)
args = argp.parse_args()
cache = Cache()
typ = {
    "A": 1,
    "NS": 2,
    "CNAME": 5,
    "MX": 15,
    "AAAA": 28,
    "TXT": 16,
}


def interactive():
    """Interactive mode"""
    help_info = [
        ("show", "show <history/like/rank/config>"),
        ("clear", "clear <history/like>"),
        (
            "query",
            "query <type> <domain> <like>, where type is A/NS/CNAME/MX/AAAA/TXT and like is 1/0",
        ),
        (
            "set",
            "set <server/port/protocol/cache/cache_file/iterative> <value>\n \
                \tNote that bool value should be represented as 1/0",
        ),
        ("exit", "Exit the cli"),
        ("help", "show help info"),
    ]
    conf = {
        "server": "8.8.8.8",
        "port": 53,
        "protocol": "udp",
        "cache": True,
        "cache_file": "cache.pickle",
        "iterative": False,
    }
    try:
        cache.load(conf["cache_file"])
    except FileNotFoundError:
        cache.save(conf["cache_file"])
        print("Default cache file not found, will be created")
    print("Welcome to DNS query tool. Type 'help' for help\n>> ", end="")
    try:
        while True:
            cmd = input().split()
            if not cmd:
                print(">> ", end="")
                continue
            if cmd[0] == "exit":
                if conf["cache"]:
                    cache.save(conf["cache_file"])
                print("Exiting...")
                return
            if cmd[0] == "help":
                print("Available commands:")
                for i in help_info:
                    print("Command:", i[0], "\tDescription:", i[1])
            elif cmd[0] == "show":
                if cmd[1] == "history":
                    for i in cache.cache:
                        print(i[0], "with type", i[1])
                elif cmd[1] == "like":
                    for i in cache.like:
                        print(i[0], "with type", i[1])
                elif cmd[1] == "rank":
                    for i in sorted(
                        cache.cache, key=lambda x: cache.cache[x][2], reverse=True
                    ):
                        print(i[0], "with type", i[1], "\t\thit", cache.cache[i][2])
                elif cmd[1] == "config":
                    print("Current configuration:\n")
                    for i in conf.items():
                        print(i[0], ":", i[1])
                else:
                    print("Invalid command")
            elif cmd[0] == "clear":
                if cmd[1] == "history":
                    cache.cache = {}
                elif cmd[1] == "like":
                    cache.like = {}
                else:
                    print("Invalid command")
            elif cmd[0] == "set":
                if cmd[1] == "cache" or cmd[1] == "iterative":
                    conf[cmd[1]] = bool(int(cmd[2]))
                    print(f"{cmd[1]} set to {conf[cmd[1]]}")
                elif cmd[1] == "cache_file":
                    conf[cmd[1]] = cmd[2]
                    try:
                        cache.load(cmd[2])
                        print("Cache file loaded")
                    except FileNotFoundError:
                        print("Cache file not found, will be created")
                elif cmd[1] in conf:
                    conf[cmd[1]] = cmd[2]
                    print(f"{cmd[1]} set to {conf[cmd[1]]}")
                else:
                    print("Invalid command")
            elif cmd[0] == "query":
                if len(cmd) == 3:
                    cmd.append(0)
                query(
                    conf["cache"],
                    cmd[2],
                    cmd[1],
                    not conf["iterative"],
                    conf["server"],
                    conf["port"],
                    conf["protocol"],
                    int(cmd[3]),
                )
            else:
                print("Invalid verb. Type 'help' for help")
            print(">> ", end="")
    except KeyboardInterrupt:
        print("\nExiting...")
        return
    # except Exception as e:
    #     print(f"Error: {e}")


def cli():
    """Command line interface"""
    try:
        if args.data == "history":
            cache.load(args.cache_file)
            for i in cache.cache:
                print(i[0], "with type", i[1])
            return
        elif args.data == "like":
            cache.load(args.cache_file)
            for i in cache.like:
                print(i[0], "with type", i[1])
            return
        elif args.data == "clear":
            cache.load(args.cache_file)
            cache.cache = {}
            cache.like = {}
            cache.save(args.cache_file)
            return
        elif args.data == "rank":
            cache.load(args.cache_file)
            for i in sorted(cache.cache, key=lambda x: cache.cache[x][2], reverse=True):
                print(i[0], "with type", i[1], "\t\thit", cache.cache[i][2])
            return
    except FileNotFoundError:
        print("Cache file not found")
        return
    if args.cache:
        try:
            cache.load(args.cache_file)
        except FileNotFoundError:
            print("Cache file not found, will be created")
    query(
        args.cache,
        args.data,
        args.type,
        args.recursion,
        args.server,
        args.port,
        args.protocol,
        args.like,
    )
    cache.save(args.cache_file)


def query(c, data_orig, query_type, recursion, server, port, protocol, like):
    """Query operation"""
    if recursion:
        data = DNSGenerator(data_orig, typ[query_type], recursion)
        query_data = data.query
        ret_raw = DNSResult(query_data, server, port, protocol)
        if ret_raw.status == -1:
            print(f"Error: Socket error {ret_raw.answer}")
            return
        ret = DNSQuery(ret_raw.answer, protocol)
        ret.query_info()
    else:
        serv = "a.root-servers.net"
        query_data = DNSGenerator(data_orig, typ[query_type], 0).query
        while True:
            print(f"Redirecting to {serv}")
            query_ns = DNSGenerator(serv, 1, 1).query
            ret_ns = DNSResult(query_ns, server, port, protocol)
            if ret_ns.status == -1:
                print(f"Error: Socket error {ret_ns.answer}")
                return
            ns = DNSQuery(ret_ns.answer, protocol)
            ns = ns.query["answers"][0]["rdata"]
            ret = DNSResult(query_data, ns, 53, protocol)
            if ret.status == -1:
                print(f"Error: Socket error {ret.answer}")
                return
            ret = DNSQuery(ret.answer, protocol)
            if ret.query["answers"]:
                ret.query_info()
                break
            serv = ret.query["authorities"][0]["ns"][:-1]
    if c:
        cached = cache.get((data_orig, typ[query_type]))
        purged = []
        ttl = int(1e9)
        for i in ret.query["answers"]:
            purged.append(i["data"])
            ttl = min(ttl, i["ttl"])
        purged.sort()
        if cached:
            if cached != purged:
                print("Cache miss")
                tmp = purged
                for i in cached:
                    if i not in purged:
                        print(f"diff + {i}")
                    else:
                        tmp.remove(i)
                for i in tmp:
                    print(f"diff - {i}")
            else:
                print("Cache hit with no diff")
                return
        cache.set((data_orig, typ[query_type]), purged, ttl, like)


if __name__ == "__main__":
    if args.data == "cli":
        interactive()
    else:
        cli()
