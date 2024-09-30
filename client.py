from client.udp import UDPClient

def main():
	client = UDPClient("127.0.0.1",514)
	resp = client.send(b"Hello, World!")
	print(resp)

if __name__ == "__main__":
	main()