import json
import threading
import pygame
from source.web import *


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
        return set(message)

    def draw(self):
        pygame.init()
        size = 800, 800
        screen = pygame.display.set_mode(size)
        running = True
        cl = pygame.time.Clock()
        sockOut = connect_OutSocket()
        sockIn = connect_InSocket(port=5556)
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                sock_send(sockOut, event)
            print(read_sock(sockIn))
            screen.fill((0, 0, 0))
            pygame.display.flip()
            cl.tick(60)
        close_sock(sockOut)
        close_sock(sockIn)
        pygame.quit()


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
