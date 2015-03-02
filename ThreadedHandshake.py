__author__ = 'David'

import socketserver
import threading
import json


class ThreadedTCPRequestHandler(socketserver.BaseRequestHandler):
    def handle(self):
        self.request.recv(1024)
        self.request.sendall(bytes(json.dumps({'name': 'pi', 'type': 'WiFi'}), 'utf-8'))


class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    pass


class ThreadedHandshake():
    @staticmethod
    def __start(daemon):
        host, port = "localhost", 9999

        server = ThreadedTCPServer((host, port), ThreadedTCPRequestHandler)
        ip, port = server.server_address

        # Start a thread with the server -- that thread will then start one
        # more thread for each request
        server_thread = threading.Thread(target=server.serve_forever)
        # Exit the server thread when the main thread terminates
        server_thread.daemon = daemon
        server_thread.start()

        print('Server loop running in thread:', server_thread.name)

    @staticmethod
    def start():
        ThreadedHandshake.__start(False)

    @staticmethod
    def start_in_daemon_mode():
        ThreadedHandshake.__start(True)

if __name__ == "__main__":
    ThreadedHandshake.start()