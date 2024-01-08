import socket
import pickle
from threading import Thread

from libs.utils import load_config, get_local_ip


class PyShare:
    BANDWITH = 4096

    def __init__(self) -> None:
        config = load_config('config.yaml')
        self.sender_socket = self.create_socket()
        self.receiver_socket = self.create_socket()

        self.receiver = get_local_ip()
        self.receiver_port = config['receiver']['port']

        self.sender = config['sender']['address']
        self.sender_port = config['sender']['port']

        self.listen_incoming = Thread(target=self.listen, daemon=True)
        self.listen_incoming.start()

    def listen(self) -> None:
        self.receiver_socket.bind((self.receiver, self.receiver_port))
        self.receiver_socket.listen(1)
        conn, addr = self.receiver_socket.accept()

        with conn:
            while True:
                data = conn.recv(self.BANDWITH)
                if not data:
                    continue
                conn.send(b'Data is received!')
                self.data = pickle.loads(data)

    def create_socket(self) -> socket.socket:
        return socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect(self) -> None:
        self.sender_socket.connect((self.sender, self.sender_port))

    def send_obj(self, obj: object) -> bool:
        self.connect()
        serialized = pickle.dumps(obj)
        self.sender_socket.send(serialized)
        return self.sender_socket.recv(self.BANDWITH)
