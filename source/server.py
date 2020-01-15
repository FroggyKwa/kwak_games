from source.web import connect_InSocket, connect_OutSocket, read_sock, sock_send, close_sock


sockOut = connect_OutSocket(port=5556)
sockIn = connect_InSocket()


while True:
    data = read_sock(sockIn)

close_sock(sockIn)
close_sock(sockOut)