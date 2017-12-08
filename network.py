import socket

class Reader():
    def __init__(self, port, msg_len):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        self.port = port
        self.sock.bind(('0.0.0.0', self.port))
        self.msg_len = msg_len

    def read(self):
        self.sock.setblocking(False)
        try:
            return self.sock.recv(self.msg_len)
        except:
            return False


class Writer():
    def __init__(self, port):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        self.port = port

    def write(self, msg):
        self.sock.sendto(msg, ('255.255.255.255', self.port))