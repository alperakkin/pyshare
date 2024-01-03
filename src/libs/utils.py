import yaml
import socket
def load_config(path: str, loader=yaml.safe_load) -> dict:
    with open(path, 'r') as f:
        data = loader(f)
    return data


def is_server(server_address: str) -> bool:
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(('192.168.100.100', 80))
    ip = s.getsockname()[0]
    s.close()
    return ip == server_address
