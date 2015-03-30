__author__ = 'David'

import socketserver
import threading

from GpioOutputState import GpioOutputState
import IpAddress
from ThreadedTCPServer import ThreadedTCPServer


class ThreadedStateTCPRequestHandler(socketserver.BaseRequestHandler):
    def handle(self):
        self.request.sendall(bytes(GpioState(self.request.recv(1024).decode('utf-8').strip()).jsonize(), 'utf-8'))


class ThreadedState():
    @staticmethod
    def __start(daemon):
        host, port = IpAddress.get_lan_ip(), 2222
        server = ThreadedTCPServer((host, port), ThreadedStateTCPRequestHandler)
        # Start a thread with the server -- that thread will then start one
        # more thread for each request
        server_thread = threading.Thread(target=server.serve_forever)
        # Exit the server thread when the main thread terminates
        server_thread.daemon = daemon
        server_thread.start()
        print('State running.')

    @staticmethod
    def start():
        ThreadedState.__start(False)

    @staticmethod
    def start_in_daemon_mode():
        ThreadedState.__start(True)


if __name__ == '__main__':
    ThreadedState.start()
