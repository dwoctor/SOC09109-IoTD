__author__ = 'David'

import socket

host, port = 'localhost', 3333

# Create a socket (SOCK_STREAM means a TCP socket)
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect to server
sock.connect((host, port))

sock.send(bytes('{"pin": 3, "state": true}', 'UTF-8'))
