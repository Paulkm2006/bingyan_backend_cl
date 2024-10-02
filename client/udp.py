import socket

class UDPClient():
	def __init__(self, addr, port):
		self.port = port
		self.addr = addr
		self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

	def send(self, data):
		self.sock.sendto(data, (self.addr, self.port))
		self.resp = self.sock.recv(1024)