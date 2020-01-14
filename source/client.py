import socket

UDP_PORT = 5555
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.connect(('localhost', UDP_PORT))
cnt = 0
while True:
    sock.send(f'{cnt}'.encode())
    cnt += 1
