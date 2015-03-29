__author__ = 'David'

import socket

host, port = 'localhost', 1111

# Create a socket (SOCK_STREAM means a TCP socket)
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect to server
sock.connect((host, port))

# Receive data from the server and shut down
received = str(sock.recv(1024), 'utf-8')
print('Received: {}'.format(received))