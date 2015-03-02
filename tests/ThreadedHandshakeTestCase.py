__author__ = 'David'

import unittest
import socket
from ThreadedHandshake import ThreadedHandshake


class ThreadedHandshakeTestCase(unittest.TestCase):

    def testPiHandshake(self):
        ThreadedHandshake.start_in_daemon_mode()
        host, port = 'localhost', 9999
        data = 'hello'

        # Create a socket (SOCK_STREAM means a TCP socket)
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        try:
            # Connect to server and send data
            sock.connect((host, port))
            sock.sendall(bytes('{0}\n'.format(data), 'utf-8'))

            # Receive data from the server and shut down
            received = str(sock.recv(1024), 'utf-8')
        finally:
            sock.close()
        print('Sent:     {}'.format(data))
        print('Received: {}'.format(received))
        self.assertEqual({'name': 'pi', 'type': 'WiFi'}, received)

if __name__ == '__main__':
    unittest.main()
