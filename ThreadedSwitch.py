__author__ = 'David'

import json
import threading

from GpioCommand import GpioCommand
from GpioState import GpioState


class ThreadedSwitch():
    @staticmethod
    def __start():
        print('SwitchState running.')
        while True:
            switch = GpioState(json.dumps({'pin': 22}))
            if switch.state == 0:
                while switch.state == 0:
                    switch = GpioState(json.dumps({'pin': 22}))
                led = GpioState(json.dumps({'pin': 17}))
                GpioCommand(json.dumps({'pin': led.pin, 'state': not led.state})).execute()

    @staticmethod
    def start():
        threading.Thread(target=ThreadedSwitch.__start()).start()


if __name__ == '__main__':
    ThreadedSwitch.start()
