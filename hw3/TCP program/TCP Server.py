#!/usr/bin/env python
# -*- coding:utf-8 -*-

import socket
import threading
import time

ser = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

ser.bind(('127.0.0.1', 8080))

ser.listen(5)               # 监听连接 如果有超过5个连接请求，从第6个开始不会被accept

print('Server is running...')       # 打印运行提示

def tcplink(connect, addr):
    print('Accept new connection from %s:%s...' % addr)
    connect.send(b'Welcome!\r\n'+b'Please tell me your name:')
    data = connect.recv(1024)
    connect.send(('Hello, %s' % data.decode('utf-8')).encode('utf-8'))
    while True:
        data = connect.recv(1024)
        time.sleep(1)
        if not data or data.decode('utf-8') == 'exit':
            break
        print("Device: %s, Data: %s, Size: %s" % (addr[0], data.decode('utf-8'), len(data)))
        connect.send(b'Data Receive')
    connect.close()
    print('Connection from %s:%s closed' % addr)

while True:
    sock, addr = ser.accept()
    pthread = threading.Thread(target=tcplink, args=(sock, addr))   #多线程处理socket连接
    pthread.start()

