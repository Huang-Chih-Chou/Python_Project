#!/usr/bin/env python
# coding=utf-8
'''
Created on 2016-10-10
@author :   dillon
'''
import socket

host = '127.0.0.1'
mysock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
addr = (host,5555)
mysock.connect(addr)
try:
        msg =b"\nhi, This is connection from python network client \n"
        mysock.sendall(msg)

except socket.errno as e:
    print ("This is Socket Error!", e)
finally:
    mysock.close()