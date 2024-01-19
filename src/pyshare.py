import socket
import pickle
from threading import Thread

from libs.utils import get_local_ip


class PyShare:
    BANDWITH = 4096

    def __init__(self, port) -> None:
        self.sender_socket = self.create_socket()
        self.receiver_socket = self.create_socket()
        self.connected = False
        self.port = port

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

                if data.startswith(b'<request>: '):
                    obj_name = data.decode().lstrip('<request>: ')
                    obj = self.scope.get(obj_name)
                    self.send_obj(conn, obj)

    def create_socket(self) -> socket.socket:
        return socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect(self, connection) -> None:
        self.sender_socket.connect(connection)

    def send_obj(self, conn: object, obj: object) -> str:
        serialized = pickle.dumps(obj)
        conn.send(serialized)
        return conn.recv(self.BANDWITH)

    def import_from(self, connection: tuple, object_name: str) -> object:
        if not self.connected:
            self.connect(connection)
            self.connected = True
        request_string = '<request>: %s' % object_name
        self.sender_socket.send(request_string.encode())
        obj = self.sender_socket.recv(self.BANDWITH)

        return pickle.loads(obj)
