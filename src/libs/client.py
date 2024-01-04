import socket
import pickle

from io import BytesIO
class ShareClient:
    def __init__(self, config: dict) -> None:
        self.socket  = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.config = config


    def connect(self) -> None:
        server_address = self.config['server']['address']
        port = self.config['port']
        self.socket.connect((server_address, port))

    def dump_object(self, obj: object) -> BytesIO:
        f = BytesIO()
        pick = pickle.Pickler(f)
        pick.dump(obj)
        return f




    def send_obj(self, obj: object) -> bool:
        self.socket.send(self.dump_object(obj))
        received_ok  = self.socket.recv(4096)
        print(received_ok)


