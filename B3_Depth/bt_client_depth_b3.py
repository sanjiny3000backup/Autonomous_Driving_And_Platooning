# -*- coding: utf-8 -*-

import depth_b3
import socket

serverMACAddress2 = 'DC:A6:32:BD:83:6E' #PoMini Bluetooth MAC Address
port2 = 5

bt_socket2 = socket.socket(socket.AF_BLUETOOTH, socket.SOCK_STREAM, socket.BTPROTO_RFCOMM)
bt_socket2.connect((serverMACAddress2, port2))

print("시작")
while True:
    dist = str(depth_b3.depth())
    print("보내는 값 :", dist)
    bt_socket2.send(dist.encode())

bt_socket2.close()