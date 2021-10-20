#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
import time

import netifaces
from PyQt5.QtWidgets import QApplication, QInputDialog, QMainWindow, QMessageBox
from PyQt5.QtGui import QImage, QPixmap
from ui.Ui_main import Ui_MainWindow
from module.Message import MessageServer, MessageClient
from module.Video import VideoServer, VideoClient
from module.Audio import AudioClient, AudioServer
from module.Live import LiveServer, LiveClient
from module.config import *


class MyMainForm(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(MyMainForm, self).__init__(parent)
        self.setupUi(self)

        self.pushButton_start_2.clicked.connect(self.run_chat_btn)  # 聊天
        self.pushButton_start_3.clicked.connect(self.run_live_client)  # 观看广播
        self.pushButton_start.clicked.connect(
            self.run_live_desktop_btn)  # 广播桌面
        self.pushButton_start_4.clicked.connect(self.run_live_user_btn)  # 广播用户
        self.pushButton_get_ip.clicked.connect(self.get_ips)  # 获取广播地址
        self.pushButton_close.clicked.connect(self.close_all)  # 关闭连接
        self.pushButton_end.clicked.connect(self.close)  # 退出程序

        self.chat_server = None
        self.chat_client = None
        self.audio_server = None
        self.audio_client = None
        self.live_server = None
        self.live_client = None

        self.passivity = True

        self.to_ip = ''
        self.to_port = 0

        self.msg_type = ''
        self.msg_server = MessageServer(self)
        self.msg_server.start()

    def close_all(self):
        threads = [
            self.chat_client,
            self.chat_server,
            self.audio_client,
            self.audio_server,
            self.live_client,
            self.live_server
        ]
        for thread in threads:
            if thread is not None:
                thread.stop()
        self.label_video.clear()
        self.label_video_2.clear()
        self.label_video.repaint()
        self.label_video_2.repaint()

    def run_chat_btn(self):
        self.passivity = False
        self.run_chat_server()
        self.to_ip = self.lineEdit_ip.text()

        self.msg_type = 'video'
        self.msg_client_1 = MessageClient(self)
        self.msg_client_1._msg.connect(self.show_msg)
        self.msg_client_1.start()

        self.run_audio_btn()

    def run_audio_btn(self):
        self.passivity = False
        self.run_audio_server()
        self.to_ip = self.lineEdit_ip.text()

        self.msg_type = 'audio'
        self.msg_client_2 = MessageClient(self)
        self.msg_client_2._msg.connect(self.show_msg)
        self.msg_client_2.start()

    def run_chat_server(self):
        # 打开聊天服务器
        if not self.passivity:  # 主动
            ip = self.lineEdit_ip.text()
            port = configs['chat']['to_port']
        else:  # 被动
            ip = self.msg_server.from_addr[0]
            port = configs['chat']['to_port']
        self.to_ip = ip
        self.to_port = port

        if self.chat_server is None or self.chat_server.stop_run:
            # 创建聊天服务端线程
            self.chat_server = VideoServer(self)
            # 连接信号，绑定回调事件
            self.chat_server._msg.connect(self.show_msg)
            self.chat_server._video_src.connect(self.show_video_src)
            # 开始线程
            self.chat_server.start()

    def run_chat_client(self):
        # 打开聊天客户端
        if not self.passivity:  # 主动
            ip = self.lineEdit_ip.text()
            port = configs['chat']['to_port']  # int(self.lineEdit_port.text())
        else:  # 被动
            ip = self.msg_server.from_addr[0]
            port = configs['chat']['to_port']  # int(self.lineEdit_port.text())
        self.to_ip = ip
        self.to_port = port

        if self.chat_client is None or self.chat_client.stop_run:
            self.chat_client = VideoClient(self)
            self.chat_client._msg.connect(self.show_msg)
            self.chat_client._video.connect(self.show_video)
            self.chat_client.start()

    def run_audio_server(self):
        # 开启音频客户端
        if self.audio_server is None or self.audio_server.stop_run:
            self.audio_server = AudioServer(self)
            self.audio_server._msg.connect(self.show_msg)
            self.audio_server.start()

    def run_audio_client(self):
        # 开启音频客户端
        if self.audio_client is None or self.audio_client.stop_run:
            self.audio_client = AudioClient(self)
            self.audio_client._msg.connect(self.show_msg)
            self.audio_client.start()

    def run_live_desktop_btn(self):
        self.run_live_server('desktop')

    def run_live_user_btn(self):
        self.run_live_server('camera')

    def get_ips(self):
        intfs = netifaces.interfaces()

        data = []
        for intf in intfs:
            res = netifaces.ifaddresses(intf)
            if netifaces.AF_INET in res:  # ipv4
                ipv4 = res[netifaces.AF_INET][0]
                data.append('addr:' + ipv4['addr'] +
                            ',broadcast:' + ipv4['broadcast'])

        item, ok = QInputDialog.getItem(
            self, '选择广播IP', '本地IP列表：', data, 0, False)

        if ok and item:
            text = item.split(',')
            # self.lineEdit_ip.setText(text[0].split(':')[1])
            self.lineEdit_broadcast.setText(text[1].split(':')[1])

    def run_live_server(self, live_type):
        if self.live_server is None or self.live_server.stop_run:
            broadcast_ip = self.lineEdit_broadcast.text()
            self.live_server = LiveServer(broadcast_ip, live_type)
            self.live_server._msg.connect(self.show_msg)
            self.live_server._screen.connect(self.show_screen)
            self.live_server._video_src.connect(self.show_video_src)
            self.live_server.start()
        # 开启音频服务器
        if self.audio_server is None or self.audio_server.stop_run:
            self.audio_server = AudioServer(self)
            self.audio_server.start()

    def run_live_client(self):
        if self.live_client is None or self.live_client.stop_run:
            self.live_client = LiveClient()
            self.live_client._msg.connect(self.show_msg)
            self.live_client._video_src.connect(self.show_video_src)
            self.live_client._screen.connect(self.show_screen)
            self.live_client.start()
        # 开启音频客户端
        if self.audio_client is None or self.audio_client.stop_run:
            self.to_ip = self.lineEdit_ip.text()
            self.audio_client = AudioClient(self)
            self.audio_client.start()

    def show_msg(self, msg):  # 线程回调
        if msg == 'run_chat_client':
            self.run_chat_client()
        elif msg == 'run_audio_client':
            self.run_audio_client()
        elif msg == 'sock_send_1':
            self.msg_server.from_sock_1.send('1'.encode())
        elif msg == 'sock_send_2':
            self.msg_server.from_sock_2.send('2'.encode())
        print(msg)

    @staticmethod
    def img2qImg(image, size):
        # 提取图像的尺寸和通道，将openCV下的image转换成QImage
        height, width = image.shape[:2]
        bytesPerLine = 3 * width
        q_img = QImage(image.data, width, height, bytesPerLine,
                       QImage.Format_RGB888).rgbSwapped()
        # 缩放
        pixmap = QPixmap.fromImage(q_img).scaled(size)
        return pixmap

    def show_video_src(self, image):  # 线程回调

        pixmap = self.img2qImg(image, self.label_video_2.size())
        self.label_video_2.setPixmap(pixmap)
        self.label_video_2.repaint()

    def show_video(self, image):  # 线程回调

        pixmap = self.img2qImg(image, self.label_video.size())
        self.label_video.setPixmap(pixmap)
        self.label_video.repaint()

    def show_screen(self, q_image):  # 线程回调
        pixmap = QPixmap.fromImage(q_image).scaled(
            self.label_video.size(), transformMode=1)  # 平滑缩放
        self.label_video.setPixmap(pixmap)
        self.label_video.repaint()

    def closeEvent(self, event):
        # 重构closeEvent函数，关闭所有线程
        reply = QMessageBox.question(
            self, '提示', '是否要退出程序？', QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            event.accept()
            self.close_all()
            time.sleep(2)
        else:
            event.ignore()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    myWin = MyMainForm()
    myWin.show()
    sys.exit(app.exec_())
