import socket

class TCPServer():
	def __init__(self, config):
		self.config = config
		self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.sock.bind((config["host"], config["port"]))

	def run(self):
		self.sock.listen(self.config["backlog"])
		while True:
			data, addr = self.sock.accept()
			print(f"Received {data.decode()} from {addr}")
			# self.sock.send(data)