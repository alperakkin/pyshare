import socket
import pickle
class ShareServer:
    def __init__(self, config) -> None:
        self.socket  = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.host = config['server']['address']
        self.port = config['port']

    def start_server(self) -> None:
        print('Server is starting...')
        self.socket.bind((self.host, self.port))
        self.socket.listen(1)
        conn, addr = self.socket.accept()

        with conn:
            while True:
                data = conn.recv(4096)
                if not data: break
                conn.send(b'Data is received')
                data = pickle.loads(data)
                print(data)
