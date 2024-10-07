"""Simple TCP server implementation"""
import socket

class TCPServer():
    """Simple TCP server that listens for incoming connections and yields them to the caller."""
    def __init__(self, config):
        self.config = config
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind((config["host"], config["port"]))

    def run(self):
        """Run the server and yield incoming connections."""
        print(f"Listening on {self.config['host']}:{self.config['port']}")
        self.sock.listen(self.config["backlog"])
        self.sock.settimeout(1)
        while True:
            try:
                client, _ = self.sock.accept()
                data = client.recv(1024)
                yield data, client
            except socket.timeout:
                continue
            except KeyboardInterrupt:
                print("Exiting")
                break
