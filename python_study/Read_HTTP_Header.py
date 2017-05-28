# -*- coding: UTF-8 -*- 
'''
Created on 2016-10-10
@author :   dillon
'''
import socket
import re

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect(("www.google.com", 80))

http_get = b"GET / HTTP/1.1\nHost: www.google.com\n\n"
data = ''
try:
        sock.sendall(http_get)
        data = sock.recvfrom(1024)
except  socket.error:
    print ("Socket error", socket.errno)
finally:
    print("closing connection")
    sock.close()

strdata = data[0].decode("utf-8")
headers = strdata.splitlines()


for s in headers:
    print "Headers line = " + str(s)
    if re.search('Server:', s):
        print(s)