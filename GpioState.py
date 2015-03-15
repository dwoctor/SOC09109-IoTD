__author__ = 'David'

import json

try:
    import RPi.GPIO as GPIO
except RuntimeError:
    print("Error importing RPi.GPIO! You need root privileges.")


class GpioState(object):
    def __init__(self, j):
        self.__dict__ = json.loads(j)
        self.__getstate()

    def __getstate(self):
        # disable warning when pin is used in another script
        GPIO.setwarning(False)
        # Using channel numbers of the Broadcom SOC
        GPIO.setmode(GPIO.BCM)
        # pin is an output
        GPIO.setup(self.pin, GPIO.IN)
        self.__dict__['state'] = GPIO.input(self.pin)
        # print('PIN %s is %s' % (self.pin, 'ON' if self.state else 'OFF'))
        # print('PIN {} is {}'.format(self.__dict__['pin'], 'ON' if self.__dict__['state'] else 'OFF'))
        return self

    def jsonize(self):
        return json.dumps(self.__dict__)
