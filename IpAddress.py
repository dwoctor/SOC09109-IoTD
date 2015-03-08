__author__ = 'David'

# Adapted from http://stackoverflow.com/
# http://stackoverflow.com/questions/11735821/python-get-localhost-ip
# http://stackoverflow.com/a/1947766/142637

import os
import socket

if os.name != 'nt':
    import fcntl
    import struct

    def get_interface_ip(interface_name):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        return socket.inet_ntoa(fcntl.ioctl(s.fileno(), 0x8915, struct.pack('256s', interface_name[:15]))[20:24])


def get_lan_ip():
    ip = socket.gethostbyname(socket.gethostname())
    if ip.startswith('127.') and os.name != 'nt':
        interfaces = ['eth0', 'eth1', 'eth2', 'wlan0', 'wlan1', 'wifi0', 'ath0', 'ath1', 'ppp0']
        for interface_name in interfaces:
            try:
                ip = get_interface_ip(interface_name)
                break
            except IOError:
                pass
    return ip


if __name__ == '__main__':
    print(get_lan_ip())