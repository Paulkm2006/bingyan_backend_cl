from decoder.fetch_data import *
from generator.generate import *
import argparse

argp = argparse.ArgumentParser()
argp.add_argument(
    "--type",
    "-t",
    default="A",
    help="Query type",
    choices=["A", "NS", "CNAME", "MX", "AAAA", "TXT"],
)
argp.add_argument(
	"--recursion",
	"-r",
	default=True,
	help="Recursion desired",
	choices=[True, False],
)
argp.add_argument("--server", "-s", default="8.8.8.8", help="DNS server")
argp.add_argument("--port", default=53, help="DNS server port")
argp.add_argument("--protocol", default="udp", help="Protocol", choices=["udp", "tcp"])
argp.add_argument("domain", help="Domain to query")


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
	data = DNSGenerator(args.domain, typ[args.type], args.recursion)
	query = data.query
	ret_raw = DNSResult(query, args.server, args.port, args.protocol)
	if ret_raw.status == -1:
		print(f"Error: Socket error {ret_raw.answer}")
		return
	ret = DNSQuery(ret_raw.answer, args.protocol)
	ret.query_info()

if __name__ == "__main__":
	main()
