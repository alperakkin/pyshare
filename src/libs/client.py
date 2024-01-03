import socket


class ShareClient:
    def __init__(self) -> None:
        self.socket  = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

    def connect(self) -> None:
        self.socket.connect()

