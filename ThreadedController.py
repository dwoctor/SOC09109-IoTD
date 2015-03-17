__author__ = 'David'

import socketserver
import threading

from GpioCommand import GpioCommand
import IpAddress
from ThreadedTCPServer import ThreadedTCPServer


class ThreadedControllerTCPRequestHandler(socketserver.BaseRequestHandler):
    def handle(self):
        GpioCommand(self.request.recv(1024)).execute()


class ThreadedController():
    @staticmethod
    def __start(daemon):
        host, port = IpAddress.get_lan_ip(), 3333
        server = ThreadedTCPServer((host, port), ThreadedControllerTCPRequestHandler)
        ip, port = server.server_address
        # Start a thread with the server -- that thread will then start one
        # more thread for each request
        server_thread = threading.Thread(target=server.serve_forever)
        # Exit the server thread when the main thread terminates
        server_thread.daemon = daemon
        server_thread.start()
        print('Controller running.')

    @staticmethod
    def start():
        ThreadedController.__start(False)

    @staticmethod
    def start_in_daemon_mode():
        ThreadedController.__start(True)


if __name__ == '__main__':
    ThreadedController.start()
