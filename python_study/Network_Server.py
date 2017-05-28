#!/usr/bin/env python
# coding=utf-8
'''
Created on 2016-10-10
@author :   dillon
'''
import socket

# listening on local port 5555
size = 512
host = '127.0.0.1'
port = 5555

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)
sock.bind((host,port))

# max concurrent connection = 5 
sock.listen(5)
c, addr = sock.accept()
# data received from client
data = c.recv(size)

print "Connected from client IP Address:" + str(addr)
print "Data Received from Connection:" + data

if data <> "": # write received message into file
    f = open("Received.dat", 'w')
    f.write(addr[0])
    f.write("\n data received from the client:")
    f.write(data)
    f.close()

sock.close()