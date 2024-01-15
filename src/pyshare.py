import socket
import pickle
from threading import Thread
from queue import Queue
from libs.utils import load_config, get_local_ip


class PyShare:
    BANDWITH = 4096

    def __init__(self) -> None:
        config = load_config('config.yaml')
        self.sender_socket = self.create_socket()
        self.receiver_socket = self.create_socket()
        self.connected = False

        self.receiver = get_local_ip()
        self.receiver_port = config['receive']['port']

        self.sender = config['to_send']['address']
        self.sender_port = config['to_send']['port']

        self.listen_incoming = Thread(target=self.listen, daemon=True)
        self.listen_incoming.start()
        self.queue = Queue()

    def listen(self) -> None:
        self.receiver_socket.bind((self.receiver, self.receiver_port))
        self.receiver_socket.listen(1)
        conn, addr = self.receiver_socket.accept()

        with conn:
            while True:
                data = conn.recv(self.BANDWITH)
                if not data:
                    continue
                if data.startswith(b'<request>: '):
                    obj = eval(data.decode().lstrip('<request>: '))
                    res = self.send_obj(obj, (self.receiver,
                                              self.receiver_port))
                    print('PyObject is sent: %s ' % res)
                else:
                    conn.send(b'Data is received!')
                    self.queue.put(pickle.loads(data))

    def create_socket(self) -> socket.socket:
        return socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect(self, connection) -> None:
        self.sender_socket.connect(connection)

    def send_obj(self, obj: object, connection: tuple) -> str:
        if not self.connected:
            self.connect(connection)
            self.connected = True
        serialized = pickle.dumps(obj)
        self.sender_socket.send(serialized)
        return self.sender_socket.recv(self.BANDWITH)

    def receive_obj(self) -> object:
        return self.queue.get()

    def import_from(self, object_name: str, connection: tuple) -> object:
        if not self.connected:
            self.connect(connection)
            self.connected = True
        self.sender_socket.send(b'<request>: %s' % object_name)
        return self.sender_socket.recv(self.BANDWITH)
