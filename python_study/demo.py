#!/usr/bin/env python
# coding=utf-8
'''
Created on 2016-10-10
@author :   dillon
'''
import socket
target_host = "www.google.com"
target_post = 80
#建立socket 物件
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#讓client 連線
client.connect((target_host,target_post))

#傳送一些資料
client.send("GET / HTTP/1.1\r\nHost: google.com\r\n\r\n")

#接收一些資料
response = client.recv(4096)

print response