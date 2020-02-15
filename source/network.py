import socket

alive = False


def connect_InSocket(address='0.0.0.0', port=5555):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind((address, port))
    return sock


def connect_tcpInSocket(address='0.0.0.0', port=4444):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind((address, port))
    return sock


def connect_OutSocket(address='0.0.0.0', port=5555):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    sock.connect((address, port))
    return sock


def connect_tcpOutSocket(address='0.0.0.0', port=4444):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((address, port))
    return sock


def sock_send(sock, msg):
    sock.send(f'{msg}'.encode())


def read_sock(sock):
    data, address = sock.recvfrom(1024)
    return data.decode(), address


def socket_reader(sock, storage):
    while alive:
        try:
            data, address = sock.recvfrom(2048)
        except OSError:
            return
        storage.append((data.decode(), address))


def close_sock(sock):
    sock.close()
