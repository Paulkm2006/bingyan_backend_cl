"""UDP client to send data to a server."""
import socket

class UDPClient():
    """UDP client to send data to a server."""
    def __init__(self, addr, port):
        self.port = port
        self.addr = addr
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.status = 0
        self.resp = None

    def send(self, data):
        """
        Sends data to a specified address and port using a UDP socket.
        This method attempts to send the provided data up to three times. If the 
        data is successfully sent, it waits for a response from the server. The 
        socket has a timeout of 3 seconds for each send attempt.
        Args:
            data (bytes): The data to be sent.
        Attributes:
            status (int): The status of the send operation. It is set to -1 if 
                          there is a timeout or socket error.
            resp (bytes or Exception): The response received from the server if 
                                       the send operation is successful, or the 
                                       exception raised in case of an error.
        Raises:
            socket.timeout: If the socket operation times out.
            socket.error: If there is an error with the socket operation.
        """
        self.sock.settimeout(3)
        try:
            for _ in range(3):
                self.status = self.sock.sendto(data, (self.addr, self.port))
                if self.status != -1:
                    self.resp = self.sock.recv(1024)
                    self.sock.close()
                    break
        except (socket.timeout, socket.error) as e:
            self.status = -1
            self.resp = e
