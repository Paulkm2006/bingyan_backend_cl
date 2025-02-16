"""Simple UDP server implementation."""

import socket


class UDPServer:
    """Simple UDP server that listens for incoming packets and yields them to the caller."""

    def __init__(self, config):
        self.config = config
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind((config["host"], config["port"]))

    def run(self):
        """Run the server and yield incoming packets."""
        print(f"Listening on {self.config['host']}:{self.config['port']}")
        self.sock.settimeout(1)
        while True:
            try:
                data, addr = self.sock.recvfrom(1024)
                # print(f"Received {data} from {addr}")
                yield data, addr
            except socket.timeout:
                continue
            except KeyboardInterrupt:
                print("Exiting")
                break
