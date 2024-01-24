import re
import socket
import pickle

from threading import Thread
from pathlib import Path

from libs.utils import get_local_ip


class PyShare:
    BANDWITH = 4096
    MAX_FILE_SIZE = 10485760

    def __init__(self, port) -> None:
        self.sender_socket = self.create_socket()
        self.receiver_socket = self.create_socket()
        self.connection = False
        self.port = port
        self.import_pattern = r"<r>(.*)</r>"
        self.file_pattern = r"<f>(.*)</f>"

        self.receiver = get_local_ip()

        self.__service = Thread(target=self.listen, daemon=True)
        self.__service.start()
        self.__scope = {}
        self.__shared_folders = []

    def attach(self, name: str, obj: object) -> None:
        self.__scope[name] = obj

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

                    obj_name = re.match(self.import_pattern, data.decode())
                    obj_name = obj_name.groups()[0]
                    obj = self.__scope.get(obj_name)

                    self.send_obj(conn, obj)

                if data.startswith(b'<f>') and data.endswith(b'</f>'):

                    source = re.match(self.file_pattern, data.decode())
                    source = Path(source.groups()[0])

                    if str(source.parent) not in self.__shared_folders:
                        self.send_msg(conn, b"<!shared>")
                        continue

                    if not source.exists():
                        self.send_msg(conn, b"<!file>")
                        continue

                    with open(source, 'rb') as f:
                        self.send_msg(conn, f.read())

    def share_folder(self, path: str) -> None:
        self.__shared_folders.append(path)

    def create_socket(self) -> socket.socket:
        return socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect(self, connection: tuple) -> None:
        if not self.connection:
            self.sender_socket.connect(connection)
            self.connection = True

    def send_msg(self, conn: object, msg: bytes) -> None:
        conn.send(msg)

    def send_obj(self, conn: object, obj: object) -> None:
        serialized = pickle.dumps(obj)
        self.send_msg(serialized)

    def import_from(self, connection: tuple, object_name: str) -> object:
        self.connect(connection)

        request_string = f'<r>{object_name}</r>'

        self.sender_socket.send(request_string.encode())
        obj = self.sender_socket.recv(self.BANDWITH)

        return pickle.loads(obj)

    def get_file(
            self, connection: tuple, source: str, destination: str
    ) -> None:

        self.connect(connection)

        request_string = f'<f>{source}</f>'

        self.sender_socket.send(request_string.encode())
        file_object = self.sender_socket.recv(self.MAX_FILE_SIZE)

        if file_object == b"<!shared>":
            raise PermissionError('Request folder is not a shared folder')

        if file_object == b"<!file>":
            raise FileExistsError('Request file does not exist')

        if len(file_object) < 1:
            raise ConnectionError('File can not be fetched for other machine')
        with open(destination, 'wb') as f:
            f.write(file_object)
