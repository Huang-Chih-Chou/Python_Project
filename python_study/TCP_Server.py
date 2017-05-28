#!/usr/bin/env python
# coding=utf-8
'''
Created on 2016-10-10
@author :   dillon
'''
import socket
import threading

bind_ip = "0.0.0.0"
bind_port = 9999

#建立socket 物件
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server.bind((bind_ip,bind_port))

server.listen(5)

print "[*] Listening on %s:%d" % (bind_ip,bind_port)

#這是我們處理client 的 thread
def handle_client(client_socket):
    # 顯示client 送來的資料
    request = client_socket.recv(1024)
    
    print "[*] Received: %s" % request
    
    # 回傳一個封包
    client_socket.send("ACK!")
    
    client_socket.close()
    
while True:
    client,addr = server.accept()

    print "[*] Accepted connection from: %s:%d" % (addr[0],addr[1])
    
    # 啟動我們的client thread 處理來的資料
    client_handler = threading.Thread(target=handle_client,args=(client,))
    client_handler.start()