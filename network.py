# -*- coding: utf-8 -*-
import socket


class Reader:
    def __init__(self, port: int, msg_len: int):
        """
        :param port: The port number.
        :param msg_len: Message length.
        """
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        self.port = port
        self.sock.bind(('0.0.0.0', self.port))
        self.msg_len = msg_len
        self.sock.setblocking(False)

    def read(self) -> bytes or bool:
        """
        Read message from listening port.

        :return: Message or False.
        """
        try:
            return self.sock.recv(self.msg_len)
        except socket.error:
            return False


class Writer:
    def __init__(self, port: int):
        """
        :param port: The port number.
        """
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        self.port = port

    def write(self, msg: bytes):
        """
        Write message to listening port.

        :param msg: Message to send.
        """
        self.sock.sendto(msg, ('255.255.255.255', self.port))
