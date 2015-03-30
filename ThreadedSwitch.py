__author__ = 'David'

import json
import threading

from GpioCommand import GpioCommand
from GpioOutputState import GpioOutputState
from GpioInputState import GpioInputState


class ThreadedSwitch():
    @staticmethod
    def __start():
        print('Switch running.')
        while True:
            switch = GpioInputState(json.dumps({'pin': 22}))
            if switch.state is False:
                while switch.state is False:
                    switch = GpioInputState(json.dumps({'pin': 22}))
                led = GpioOutputState(json.dumps({'pin': 17}))
                GpioCommand(json.dumps({'pin': led.pin, 'state': not led.state})).execute()

    @staticmethod
    def start():
        threading.Thread(target=ThreadedSwitch.__start()).start()


if __name__ == '__main__':
    ThreadedSwitch.start()
