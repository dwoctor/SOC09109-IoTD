__author__ = 'David'

import socketserver
import threading
from protocolbuffers import deviceinfo_pb2
from ThreadedTCPServer import ThreadedTCPServer

class ThreadedProtobufHandshakeTCPRequestHandler(socketserver.BaseRequestHandler):
    def handle(self):
        self.request.recv(1024)
        data = deviceinfo_pb2.DeviceInfo()
        data.name = 'pi'
        data.type = deviceinfo_pb2.DeviceInfo.WIFI
        self.request.sendall(data)


class ThreadedProtobufHandshake():
    @staticmethod
    def __start(daemon):
        host, port = "localhost", 9999

        server = ThreadedTCPServer((host, port), ThreadedProtobufHandshakeTCPRequestHandler)
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
        ThreadedProtobufHandshake.__start(False)

    @staticmethod
    def start_in_daemon_mode():
        ThreadedProtobufHandshake.__start(True)

if __name__ == "__main__":
    ThreadedProtobufHandshake.start()
