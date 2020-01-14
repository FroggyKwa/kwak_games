import socket

UDP_PORT = 5555
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(('', UDP_PORT))

while True:
    data = sock.recv(1024)
    if not data:
        break
    print(data.decode())

sock.close()