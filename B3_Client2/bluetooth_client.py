# -*- coding: utf-8 -*-

import socket

serverMACAddress = 'DC:A6:32:BD:83:6E' #PoMini Bluetooth MAC Address

port = 5
s = socket.socket(socket.AF_BLUETOOTH, socket.SOCK_STREAM, socket.BTPROTO_RFCOMM)
s.connect((serverMACAddress,port))


def server_program(data) :
    data = str(data)
    s.send(data.encode())


while True:
    data = str(input())

    if data == "0":
        break
   #s.send(bytes(text, 'UTF-8'))
    s.send(data.encode())
s.close()
