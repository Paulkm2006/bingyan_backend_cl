from client.udp import UDPClient
from client.tcp import TCPClient
import argparse

def main():
	data = args.data
	addr, port = args.destination.split(":")
	if args.protocol == "tcp":
		client = TCPClient(addr, int(port))
	else:
		client = UDPClient(addr, int(port))
	print(f"Sending {data} to {addr}:{port}")
	if args.type == "string":
		client.send(data.encode())
	elif args.type == "int":
		client.send(str(data).encode())
	elif args.type == "file":
		with open(data, "rb") as f:
			client.send(f.read())

	print(client.resp.decode())

argp = argparse.ArgumentParser()
argp.add_argument("destination", default="127.0.0.1:514", help="Server IP and port")
argp.add_argument("--type", "-t", default="string", help="Data type", choices=["string", "int", "file"])
argp.add_argument("--protocol", default="tcp", help="Protocol", choices=["udp", "tcp"])
argp.add_argument("data", help="Data to send")


if __name__ == "__main__":
    args = argp.parse_args()
    main()
