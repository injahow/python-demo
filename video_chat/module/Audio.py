#!/usr/bin/python3
# -*- coding: utf-8 -*-

import socket
import zlib

from pyaudio import paInt16, PyAudio
from PyQt5.QtCore import QThread, pyqtSignal
from .config import *

CHUNK = 1024
FORMAT = paInt16    # 格式
CHANNELS = 2    # 输入/输出通道数
RATE = 44100    # 音频数据的采样频率


class AudioServer(QThread):  # 发送方，服务器
    _msg = pyqtSignal(str)

    def __init__(self, main_self):
        super(AudioServer, self).__init__()
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.p = PyAudio()
        self.main_self = main_self
        self.stream = None
        self.stop_run = False
        self.wait_recv = True

    def __del__(self):
        self.stop()
        if self.sock is not None:
            self.sock.close()
        if self.stream is not None:
            try:
                self.stream.stop_stream()
                self.stream.close()
            except:
                pass
        if self.p is not None:
            try:
                self.p.terminate()
            except:
                pass
        #self.wait()

    def stop(self):
        self.stop_run = True
        self.wait_recv = False

    def run(self):

        print('AudioServer bind starts...')

        self.sock.bind(('', configs['audio']['port']))
        self.sock.settimeout(1)

        if self.main_self.passivity:
            self._msg.emit('sock_send_2')

        while self.wait_recv:
            try:
                data, cli_address = self.sock.recvfrom(1024)
                self.wait_recv = False
            except:
                pass
        if self.stop_run:
            return

        print('AudioServer connected from %s:%s' % cli_address)

        self.stream = self.p.open(
            format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK)
        while self.stream.is_active() and not self.stop_run:
            data = self.stream.read(CHUNK*10)
            data = zlib.compress(data)
            self.sock.sendto(data, cli_address)
            self.msleep(40)

        self.sock.close()


class AudioClient(QThread):  # 接收方，客户端
    _msg = pyqtSignal(str)

    def __init__(self, main_self):
        super(AudioClient, self).__init__()

        self.main_self = main_self
        self.to_addr = (main_self.to_ip, configs['audio']['to_port'])
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.p = PyAudio()
        self.stream = None
        self.stop_run = False
        self.wait_recv = True

    def __del__(self):
        self.sock.close()
        if self.stream is not None:
            try:
                self.stream.stop_stream()
                self.stream.close()
            except:
                pass
        if self.p is not None:
            try:
                self.p.terminate()
            except:
                pass
        #self.wait()

    def run(self):
        print('AudioClient starts...')

        msg = '给我音频'
        self.sock.sendto(msg.encode(), self.to_addr)

        print('AudioClient connected to %s:%s' % self.to_addr)

        self.stream = self.p.open(
            format=FORMAT, channels=CHANNELS, rate=RATE, output=True, frames_per_buffer=CHUNK)

        self.sock.settimeout(1)
        while not self.stop_run:

            while self.wait_recv:
                try:
                    frame_data = self.sock.recv(1024*100)
                    self.wait_recv = False
                except:
                    pass
            self.wait_recv = True

            if self.stop_run:
                break
            frame_data = zlib.decompress(frame_data)
            self.stream.write(frame_data, CHUNK*10)

    def stop(self):
        print('AudioClient close ...')
        self.wait_recv = False
        self.stop_run = True
