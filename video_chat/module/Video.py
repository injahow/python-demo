#!/usr/bin/python3
# -*- coding: utf-8 -*-

import socket
import sys
import zlib

import numpy as np
import cv2
from PyQt5.QtCore import QThread, pyqtSignal
from .config import *


class VideoServer(QThread):  # 视频发送方
    #  定义信号
    _msg = pyqtSignal(str)
    _video_src = pyqtSignal(np.ndarray)

    def __init__(self, main_self):
        super(VideoServer, self).__init__()
        self.main_self = main_self
        self.to_ip = main_self.to_ip
        self.to_port = main_self.to_port
        self.stop_run = False
        self.wait_recv = True
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def __del__(self):
        self.stop()
        #self.wait()

    def stop(self):
        print('VideoServer close ...')
        self.wait_recv = False
        self.stop_run = True

    def run(self):  # 发送
        # 本地UDP监听

        self.sock.bind(('', configs['chat']['port']))
        print('VideoServer run ...')
        self.sock.settimeout(1)

        if self.main_self.passivity:
            self._msg.emit('sock_send_1')

        while self.wait_recv:
            try:
                data, cli_address = self.sock.recvfrom(1024)
                self.wait_recv = False
            except:
                pass
        if self.stop_run:
            self.sock.close()
            return

        print('VideoServer connected from %s:%s' % cli_address)

        # 打开摄像头
        cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
        # 压缩比：0~100
        jpeg_quality = 20
        params = [cv2.IMWRITE_JPEG_QUALITY, jpeg_quality]

        while not self.stop_run:
            ret, frame = cap.read()
            frame = cv2.resize(frame, (1280, 720))
            if self.stop_run:
                break
            # 本地回调显示
            self._video_src.emit(frame)

            data_encode = cv2.imencode('.jpg', frame, params)[1]  # 数据打包
            str_encode = data_encode.tobytes()
            # udp数据包最大支持65507
            str_encode = zlib.compress(str_encode)
            if sys.getsizeof(str_encode) > 65507:
                continue
            self.sock.sendto(str_encode, cli_address)
            self.msleep(40)

        # 结束捕获
        cap.release()
        self.sock.close()


class VideoClient(QThread):  # 视频接收方
    #  定义信号
    _msg = pyqtSignal(str)
    _video = pyqtSignal(np.ndarray)

    def __init__(self, main_self):
        super(VideoClient, self).__init__()
        if main_self.passivity:  # 被动启动
            self.to_ip = main_self.msg_server.from_addr[0]
            self.to_port = configs['chat']['to_port']
        else:
            self.to_ip = main_self.to_ip
            self.to_port = configs['chat']['to_port']
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.stop_run = False

    def __del__(self):
        self.stop()
        #self.wait()

    def stop(self):
        print('VideoClient close ...')
        self.wait_recv = False
        self.stop_run = True

    def run(self):  # 接收

        msg = '给我视频'
        server_address = (self.to_ip, self.to_port)
        self.sock.sendto(msg.encode(), server_address)

        self.sock.settimeout(1)
        while not self.stop_run:
            while self.wait_recv:
                try:
                    receive_data = self.sock.recv(1024*100)  # , address
                    self.wait_recv = False
                except:
                    pass
            self.wait_recv = True

            receive_data = zlib.decompress(receive_data)
            image = np.frombuffer(receive_data, np.uint8)
            image = cv2.imdecode(image, cv2.IMREAD_COLOR)
            # 将视频图片回调给主进程
            if self.stop_run:
                break
            self._video.emit(image)

        self.sock.close()
