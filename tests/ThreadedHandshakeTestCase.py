__author__ = 'David'

import unittest
import socket

from ThreadedHandshake import ThreadedHandshake


class ThreadedHandshakeTestCase(unittest.TestCase):
    def testPiHandshake(self):
        ThreadedHandshake.start_in_daemon_mode()
        host, port = 'localhost', 1111

        # Create a socket (SOCK_STREAM means a TCP socket)
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        try:
            # Connect to server
            sock.connect((host, port))

            # Receive data from the server and shut down
            received = str(sock.recv(1024), 'utf-8')
        finally:
            sock.close()
        print('Received: {}'.format(received))
        self.assertEqual({'name': 'pi', 'type': 'wifi', 'capability': 'gpio'}, received)


if __name__ == '__main__':
    unittest.main()
