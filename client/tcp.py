import socket

class TCPClient():

    def __init__(self, addr, port):
        self.port = port
        self.addr = addr
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def send(self, data):
        self.sock.connect((self.addr, self.port))
        self.sock.send(data)
        self.resp = self.sock.recv(1024)
