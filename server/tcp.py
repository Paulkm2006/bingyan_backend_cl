import socket

class TCPServer():
    def __init__(self, config):
        self.config = config
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind((config["host"], config["port"]))

    def run(self):
        print(f"Listening on {self.config['host']}:{self.config['port']}")
        self.sock.listen(self.config["backlog"])
        self.sock.settimeout(1)
        while True:
            try:
                client, addr = self.sock.accept()
                data = client.recv(1024)
                yield data, client
            except socket.timeout:
                continue
            except KeyboardInterrupt:
                print("Exiting")
                break
