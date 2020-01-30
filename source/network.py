import socket
import json
import threading


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


def read_server_sock(sock, storage, alive):
    while alive:
        data, address = sock.recvfrom(2048)
        storage.append((data.decode(), address))
        if not alive:  # TODO: УДАЛИТЬ
            return


def close_sock(sock):
    sock.close()


class Client:
    def __init__(self, server_host, server_port_udp=1234, client_port_udp=1235):
        self.identifier = None
        self.server_message = []
        self.room_id = None
        self.client_udp = ("localhost", client_port_udp)
        self.lock = threading.Lock()
        self.server_listener = SocketThread(self.client_udp, self, self.lock)
        self.server_listener.start()
        self.server_udp = (server_host, server_port_udp)

    def send(self, msg):
        message = json.dumps({
            "action": "send",
            "message": msg,
            "identifier": self.identifier
        })
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.sendto(message.encode(), self.server_udp)

    def get_messages(self):
        message = self.server_message
        self.server_message.clear()
        return message


class SocketThread(threading.Thread):
    def __init__(self, addr, client, lock):

        threading.Thread.__init__(self)
        self.client = client
        self.lock = lock
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind(addr)

    def run(self):
        while True:
            data, addr = self.sock.recvfrom(1024)
            self.lock.acquire()
            try:
                self.client.server_message.append(data)
            finally:
                self.lock.release()

    def stop(self):
        self.sock.close()
