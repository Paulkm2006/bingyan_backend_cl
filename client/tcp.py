import socket

class TCPClient():

    def __init__(self, addr, port):
        self.port = port
        self.addr = addr
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def send(self, data):
        self.sock.settimeout(3)
        try:
            for i in range(3):
                self.sock.connect((self.addr, self.port))
                self.status = self.sock.send(data)
                if self.status != -1:
                    self.resp = self.sock.recv(1024)
                    self.sock.close()
                    break
        except Exception as e:
            self.status = -1
            self.resp = e
