#! /bin/bash

mkdir -p /etc/systemd/system/
mkdir -p /usr/local/bin/

cp /root/SOC09109-IoTD/netboot.service /etc/systemd/system/netboot.service
cp /root/SOC09109-IoTD/netboot.sh /usr/local/bin/netboot.sh

chmod 755 /etc/systemd/system/netboot.service
chmod 755 /usr/local/bin/netboot.sh

systemctl enable /etc/systemd/system/netboot.service
