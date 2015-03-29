__author__ = 'David'

import json
import socket
import threading

from GpioState import GpioState


class ThreadedSwitchState():
    @staticmethod
    def __start():
        print('SwitchState running.')
        destination = ('<broadcast>', 4444)
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        while True:
            s.sendto(bytes(GpioState(json.dumps({'pin': 22})).jsonize(), 'utf-8'), destination)

    @staticmethod
    def start():
        threading.Thread(target=ThreadedSwitchState.__start()).start()


if __name__ == '__main__':
    ThreadedSwitchState.start()
