#!/usr/bin/env python
# coding=utf-8
'''
Created on 2016-10-10
@author :   dillon
'''
import socket
target_host = "127.0.0.1"
target_post = 80
#建立socket 物件
client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

#傳送一些資料
client.sendto("AAABBB",(target_host,target_post))

#接收一些資料
data , addr = client.recvfrom(4096)

print data