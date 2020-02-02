import socket
import json
import threading

alive = False

def connect_InSocket(address='0.0.0.0', port=5555):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    sock.bind((address, port))
    return sock


def connect_OutSocket(address='0.0.0.0', port=5555):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    sock.connect((address, port))
    return sock


def sock_send(sock, msg):
    sock.send(f'{msg}'.encode())


def read_sock(sock):
    data, address = sock.recvfrom(1024)
    return data.decode(), address


def read_server_sock(sock, storage):
    while alive:
        data, address = sock.recvfrom(2048)
        storage.append((data.decode(), address))
        if not alive:  # TODO: УДАЛИТЬ
            return


def close_sock(sock):
    sock.close()