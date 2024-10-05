import socket

class TCPClient():

    def __init__(self, addr, port):
        self.port = port
        self.addr = addr
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.status = 0
        self.resp = None

    def send(self, data):
        """
        Sends data to the server and handles the response.

        This method attempts to send the provided data to the server up to three times.
        It sets a timeout of 3 seconds for each attempt. If the data is successfully sent,
        it waits for a response from the server. If any socket timeout or error occurs,
        it sets the status to -1 and stores the exception in the response.

        Args:
            data (bytes): The data to be sent to the server.

        Attributes:
            status (int): The status of the send operation. -1 indicates failure.
            resp (bytes or Exception): The response from the server or the exception if an error occurred.
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
