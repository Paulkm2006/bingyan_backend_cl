import socket

class UDPServer():
	def __init__(self, config):
		self.config = config
		self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		self.sock.bind((config["host"], config["port"]))

	def run(self):
		print(f"Listening on {self.config['host']}:{self.config['port']}")
		while True:
			data, addr = self.sock.recvfrom(1024)
			print(f"Received {data} from {addr}")
			self.sock.sendto(data, addr)