import socket


def get_local_ip() -> str:
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(('192.168.100.100', 80))
    ip = s.getsockname()[0]
    s.close()
    return ip
