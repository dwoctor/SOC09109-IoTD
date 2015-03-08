__author__ = 'David'

import json
import socketserver
import threading

import IpAddress
from ThreadedTCPServer import ThreadedTCPServer


class ThreadedHandshakeTCPRequestHandler(socketserver.BaseRequestHandler):
    def handle(self):
        self.request.recv(1024)
        self.request.sendall(bytes(json.dumps({'name': 'pi', 'type': 'wifi'}), 'utf-8'))


class ThreadedHandshake():
    @staticmethod
    def __start(daemon):
        host, port = IpAddress.get_lan_ip(), 1111
        server = ThreadedTCPServer((host, port), ThreadedHandshakeTCPRequestHandler)
        ip, port = server.server_address
        # Start a thread with the server -- that thread will then start one
        # more thread for each request
        server_thread = threading.Thread(target=server.serve_forever)
        # Exit the server thread when the main thread terminates
        server_thread.daemon = daemon
        server_thread.start()
        print('Handshake running.')


    @staticmethod
    def start():
        ThreadedHandshake.__start(False)

    @staticmethod
    def start_in_daemon_mode():
        ThreadedHandshake.__start(True)


if __name__ == '__main__':
    ThreadedHandshake.start()
