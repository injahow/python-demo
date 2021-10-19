#!/usr/bin/python3
# -*- coding: utf-8 -*-

import threading
import socket
import sys

from PyQt5.QtCore import QThread, pyqtSignal
from .config import *


class MessageServer(QThread):  # 信息接收者
    # _msg = pyqtSignal(str)

    def __init__(self, main_self):
        super(MessageServer, self).__init__()
        self.main_self = main_self
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.from_sock_1 = None
        self.from_sock_2 = None
        self.from_addr = ()

    def __del__(self):
        pass
        #self.wait()

    def tcp_link(self, sock, addr):
        # 判断本地连接状况，返回0表示不连接
        data = sock.recv(1024).decode()

        if data == '1':  # 请求方已经启动了视频服务器，希望建立通话
            if self.main_self.chat_client is None and self.main_self.chat_server is None:
                self.from_sock_1 = sock
                self.from_addr = addr
                self.main_self.passivity = True
                self.main_self.run_chat_server()
                self.main_self.run_chat_client()
            else:
                sock.send('0'.encode())
                sock.close()

        elif data == '2':  # 请求方已经启动了音频服务器，希望建立通话
            if self.main_self.audio_client is None and self.main_self.audio_server is None:
                self.from_sock_2 = sock
                self.from_addr = addr
                self.main_self.passivity = True
                self.main_self.run_audio_server()
                self.main_self.run_audio_client()
            else:
                sock.send('0'.encode())
                sock.close()
        else:
            # todo
            sock.close()

    def run(self):
        try:
            self.sock.bind(('', configs['msg']['port']))
        except socket.error:
            print('MessageServer failed')
            sys.exit()
        print('MessageServer bind complete')
        self.sock.listen(10)
        while True:
            # 接受新的TCP连接，创建新线程
            conn, addr = self.sock.accept()
            print('Accept Message connection from %s:%s ' % addr)
            link = threading.Thread(target=self.tcp_link, args=(conn, addr))
            link.setDaemon(True)
            link.start()


class MessageClient(QThread):  # 信息发起者
    _msg = pyqtSignal(str)

    def __init__(self, main_self):
        super(MessageClient, self).__init__()
        self.main_self = main_self
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.to_ip = main_self.to_ip
        self.msg_type = main_self.msg_type

    def __del__(self):
        pass
        #self.wait()
        
    def run(self):

        self.sock.connect((self.to_ip, configs['msg']['to_port']))
        print('MessageClient connect to ' + self.to_ip)
        if self.msg_type == 'video':
            msg_str = '1'
            callback_str = 'run_chat_client'
        elif self.msg_type == 'audio':
            msg_str = '2'
            callback_str = 'run_audio_client'

        self.sock.send(msg_str.encode())
        data = self.sock.recv(1024).decode()

        if data == msg_str:  # 同意连接
            self._msg.emit(callback_str)
        self.sock.close()
