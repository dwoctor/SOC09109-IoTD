#! /bin/bash

exec &> /root/SOC09109-IoTD/errorlog.txt

loadkeys uk
netctl start wlan0-Raspberry
python /root/SOC09109-IoTD/Start.py
