from decoder.fetch_data import *
from generator.generate import *
from cache import *
import argparse

root_server = "a.root-servers.net" # ICAAN

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
argp.add_argument("--no-cache", "-nc", dest="cache", action="store_false", help="Disable cache")
argp.add_argument("--cache-file", "-f", default="cache.pickle", help="Cache file")
argp.add_argument("--like", "-l", action="store_true", help="Add query into likes (requires cache)")
argp.add_argument(
    "data",
    help="Domain to query/command(history, like, rank, clear)",
)


def main():
    typ = {
        "A": 1,
        "NS": 2,
        "CNAME": 5,
        "MX": 15,
        "AAAA": 28,
        "TXT": 16,
    }
    args = argp.parse_args()
    if args.data == "history":
        cache = Cache()
        cache.load(args.cache_file)
        for i in cache.cache:
            print(i)[0]
        return
    elif args.data == "like":
        cache = Cache()
        cache.load(args.cache_file)
        for i in cache.like:
            print(i)
        return
    elif args.data == "clear":
        cache = Cache()
        cache.load(args.cache_file)
        cache.cache = {}
        cache.like = {}
        cache.save(args.cache_file)
        return
    elif args.data == "rank":
        cache = Cache()
        cache.load(args.cache_file)
        for i in sorted(cache.cache, key=lambda x: cache.cache[x][2], reverse=True):
            print(i[0], 'with hits', cache.cache[i][2])
        return
    if args.cache:
        cache = Cache()
        try:
            cache.load(args.cache_file)
        except FileNotFoundError:
            print("Cache file not found, will be created")
    if args.recursion:
        data = DNSGenerator(args.data, typ[args.type], args.recursion)
        query = data.query
        ret_raw = DNSResult(query, args.server, args.port, args.protocol)
        if ret_raw.status == -1:
            print(f"Error: Socket error {ret_raw.answer}")
            return
        ret = DNSQuery(ret_raw.answer, args.protocol)
        ret.query_info()
    else:
        serv = root_server
        query = DNSGenerator(args.data, typ[args.type], 0).query
        while True:
            print(f"Redirecting to {serv}")
            query_ns = DNSGenerator(serv, 1, 1).query
            ret_ns = DNSResult(query_ns, args.server, args.port, args.protocol)
            if ret_ns.status == -1:
                print(f"Error: Socket error {ret_ns.answer}")
                return
            ns = DNSQuery(ret_ns.answer, args.protocol)
            ns = ns.query["answers"][0]["rdata"]
            ret = DNSResult(query, ns, 53, args.protocol)
            if ret.status == -1:
                print(f"Error: Socket error {ret.answer}")
                return
            ret = DNSQuery(ret.answer, args.protocol)
            if ret.query["answers"]:
                if ret.query["answers"][0]["type"] == typ[args.type]:
                    ret.query_info()
                    break
            serv = ret.query["authorities"][0]["ns"][:-1]
    if args.cache:
        cached = cache.get((args.data, typ[args.type]))
        purged = []
        ttl = int(1e9)
        for i in ret.query["answers"]:
            purged.append(i["rdata"])
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
                cache.save(args.cache_file)
                return
        cache.set((args.data, typ[args.type]), purged, ttl, args.like)
        cache.save(args.cache_file)


if __name__ == "__main__":
    main()
