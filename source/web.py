import socket


def connect_InSocket(address='', port=5555):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((address, port))
    return sock


def connect_OutSocket(address='localhost', port=5555):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.connect((address, port))
    return sock


def sock_send(sock, msg):
    sock.send(f'{msg}'.encode())


def read_sock(sock):
    data = sock.recv(1024)
    return data


def close_sock(sock):
    sock.close()

