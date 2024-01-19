import re
import socket
import pickle
from threading import Thread

from libs.utils import get_local_ip


class PyShare:
    BANDWITH = 4096

    def __init__(self, port) -> None:
        self.sender_socket = self.create_socket()
        self.receiver_socket = self.create_socket()
        self.connection = False
        self.port = port
        self.pattern = r"<r>(.*)</r>"

        self.receiver = get_local_ip()

        self.listen_incoming = Thread(target=self.listen, daemon=True)
        self.listen_incoming.start()
        self.scope = {}

    def attach(self, name: str, obj: object) -> None:
        self.scope[name] = obj

    def listen(self) -> None:

        self.receiver_socket.bind((self.receiver, self.port))
        self.receiver_socket.listen(1)

        conn, addr = self.receiver_socket.accept()

        with conn:
            while True:
                data = conn.recv(self.BANDWITH)
                if not data:
                    continue

                if data.startswith(b'<r>') and data.endswith(b'</r>'):

                    obj_name = re.match(self.pattern, data.decode())
                    obj_name = obj_name.groups()[0]
                    obj = self.scope.get(obj_name)

                    self.send_obj(conn, obj)

    def create_socket(self) -> socket.socket:
        return socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect(self, connection) -> None:
        self.sender_socket.connect(connection)
        self.connection = True

    def send_obj(self, conn: object, obj: object) -> str:
        serialized = pickle.dumps(obj)
        conn.send(serialized)

    def import_from(self, connection: tuple, object_name: str) -> object:
        if not self.connection:
            self.connect(connection)
            self.connection = True

        request_string = f'<r>{object_name}</r>'

        self.sender_socket.send(request_string.encode())
        obj = self.sender_socket.recv(self.BANDWITH)

        return pickle.loads(obj)
