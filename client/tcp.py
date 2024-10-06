"""TCP client to send data to a server."""

import socket


class TCPClient:
    """TCP client to send data to a server."""

    def __init__(self, addr, port):
        self.port = port
        self.addr = addr
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.status = 0
        self.resp = None

    def send(self, data):
        """
        Sends data to the server and waits for a response.
        This method attempts to send the provided data to the server specified by
        the instance's address and port. It will try to connect and send the data
        up to three times. If the data is successfully sent, it waits for a response
        from the server. If any socket timeout or error occurs, it sets the status
        to -1 and captures the exception.
        Args:
            data (bytes): The data to be sent to the server.
        Attributes:
            status (int): The status of the send operation. -1 if an error occurred.
            resp (bytes or Exception): The response from the server if successful,
                                       otherwise the exception that was raised.
        """
        
        self.sock.settimeout(3)
        try:
            for _ in range(3):
                self.sock.connect((self.addr, self.port))
                self.status = self.sock.send(data)
                if self.status != -1:
                    self.resp = self.sock.recv(1024)
                    self.sock.close()
                    break
        except (socket.timeout, socket.error) as e:
            self.status = -1
            self.resp = e
