#!/usr/bin/python3
# -*- coding: utf-8 -*-

import socket
import sys
import zlib

import cv2
from numpy import ndarray

from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QImage, QImageReader
from PyQt5.QtCore import QBuffer, QByteArray, QIODevice, QThread, pyqtSignal
from .config import *


class LiveServer(QThread):  # 直播发送方
    #  定义信号
    _msg = pyqtSignal(str)
    _video_src = pyqtSignal(ndarray)
    _screen = pyqtSignal(QImage)

    def __init__(self, ip, live_type='camera'):
        super(LiveServer, self).__init__()
        self.broadcast_ip = ip
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        self.stop_run = False
        self.live_type = live_type  # 'desktop' or 'camera'

    def __del__(self):
        self.stop()
        #self.wait()

    def stop(self):
        print('LiveServer stop')
        self.stop_run = True

    @staticmethod
    def qImg2bytes(q_img):
        # 获取一个空的字节数组
        byte_array = QByteArray()
        # 将字节数组绑定到输出流上
        qImg_buffer = QBuffer(byte_array)
        qImg_buffer.open(QIODevice.WriteOnly)
        # 将数据使用jpg格式进行保存
        q_img.save(qImg_buffer, 'jpg', quality=32)  # 1-100
        return byte_array.data()

    def run(self):

        # 广播地址
        network = self.broadcast_ip  # '192.168.31.255'

        if self.live_type == 'camera':
            # 打开摄像头
            cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
            while not self.stop_run:
                ret, frame = cap.read()
                image = cv2.resize(frame, (1280, 720))
                # 本地回调摄像头图片
                self._video_src.emit(frame)

                height, width = image.shape[:2]
                bytesPerLine = 3 * width
                q_img = QImage(image.data, width, height, bytesPerLine,
                               QImage.Format_RGB888).rgbSwapped()
                send_data = self.qImg2bytes(q_img)

                send_data = zlib.compress(send_data)
                if sys.getsizeof(send_data) > 65507:
                    continue
                self.sock.sendto(
                    send_data, (network, configs['live']['to_port']))
                self.msleep(40)
            cap.release()
        elif self.live_type == 'desktop':
            # 设置桌面截图
            screen = QApplication.primaryScreen()

            while not self.stop_run:
                win_id = QApplication.desktop().winId()
                q_img = screen.grabWindow(win_id).scaled(
                    1280, 720, transformMode=1).toImage()
                # 本地回调桌面图片QPixmap缩小 -> QImage格式
                if self.stop_run:
                    break
                self._screen.emit(q_img)

                send_data = self.qImg2bytes(q_img)

                send_data = zlib.compress(send_data)
                if sys.getsizeof(send_data) > 65507:
                    continue

                self.sock.sendto(
                    send_data, (network, configs['live']['to_port']))
                self.msleep(40)

        self.sock.close()


class LiveClient(QThread):  # 直播接收方
    #  定义信号
    _msg = pyqtSignal(str)
    _video_src = pyqtSignal(ndarray)
    _screen = pyqtSignal(QImage)

    def __init__(self):
        super(LiveClient, self).__init__()
        self.stop_run = False
        self.wait_recv = True
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def __del__(self):
        self.stop()
        #self.wait()

    def stop(self):
        print('LiveClient stop')
        self.stop_run = True
        self.wait_recv = False

    def run(self):

        self.sock.bind(('', configs['live']['port']))
        self.sock.settimeout(1)

        print('LiveClient bind in ', self.sock.getsockname())

        while not self.stop_run:

            while self.wait_recv:
                try:
                    receive_data = self.sock.recv(1024*100)  # , address
                    self.wait_recv = False
                except:
                    pass
            self.wait_recv = True

            if self.stop_run:
                break

            receive_data = zlib.decompress(receive_data)

            byte_array = QByteArray(receive_data)
            buffer = QBuffer(byte_array)
            buffer.open(QIODevice.ReadOnly)
            # 读取图片
            reader = QImageReader(buffer)
            q_img = reader.read()
            if self.stop_run:
                break
            self._screen.emit(q_img)

        self.sock.close()  # 关闭套接字
