# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'd:\Users\injah\Documents\GitHub\python-demo\video_chat\ui\main.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1020, 800)
        MainWindow.setMinimumSize(QtCore.QSize(1020, 800))
        MainWindow.setMaximumSize(QtCore.QSize(1020, 800))
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.label_video = QtWidgets.QLabel(self.centralwidget)
        self.label_video.setGeometry(QtCore.QRect(30, 190, 960, 540))
        self.label_video.setFrameShape(QtWidgets.QFrame.Box)
        self.label_video.setFrameShadow(QtWidgets.QFrame.Plain)
        self.label_video.setText("")
        self.label_video.setIndent(-1)
        self.label_video.setObjectName("label_video")
        self.label_video_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_video_2.setGeometry(QtCore.QRect(760, 30, 231, 135))
        self.label_video_2.setFrameShape(QtWidgets.QFrame.Box)
        self.label_video_2.setText("")
        self.label_video_2.setObjectName("label_video_2")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(30, 170, 121, 16))
        self.label_3.setObjectName("label_3")
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(760, 10, 131, 21))
        self.label_4.setObjectName("label_4")
        self.groupBox = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox.setGeometry(QtCore.QRect(30, 20, 711, 141))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.groupBox.setFont(font)
        self.groupBox.setObjectName("groupBox")
        self.pushButton_start_4 = QtWidgets.QPushButton(self.groupBox)
        self.pushButton_start_4.setGeometry(QtCore.QRect(390, 80, 91, 41))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.pushButton_start_4.setFont(font)
        self.pushButton_start_4.setObjectName("pushButton_start_4")
        self.pushButton_end = QtWidgets.QPushButton(self.groupBox)
        self.pushButton_end.setGeometry(QtCore.QRect(600, 20, 101, 101))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.pushButton_end.setFont(font)
        self.pushButton_end.setObjectName("pushButton_end")
        self.lineEdit_ip = QtWidgets.QLineEdit(self.groupBox)
        self.lineEdit_ip.setGeometry(QtCore.QRect(90, 20, 191, 41))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.lineEdit_ip.setFont(font)
        self.lineEdit_ip.setObjectName("lineEdit_ip")
        self.lineEdit_broadcast = QtWidgets.QLineEdit(self.groupBox)
        self.lineEdit_broadcast.setGeometry(QtCore.QRect(90, 80, 191, 41))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.lineEdit_broadcast.setFont(font)
        self.lineEdit_broadcast.setObjectName("lineEdit_broadcast")
        self.pushButton_start = QtWidgets.QPushButton(self.groupBox)
        self.pushButton_start.setGeometry(QtCore.QRect(290, 80, 91, 41))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.pushButton_start.setFont(font)
        self.pushButton_start.setObjectName("pushButton_start")
        self.label = QtWidgets.QLabel(self.groupBox)
        self.label.setGeometry(QtCore.QRect(10, 20, 71, 41))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.pushButton_start_3 = QtWidgets.QPushButton(self.groupBox)
        self.pushButton_start_3.setGeometry(QtCore.QRect(390, 20, 91, 41))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.pushButton_start_3.setFont(font)
        self.pushButton_start_3.setObjectName("pushButton_start_3")
        self.label_2 = QtWidgets.QLabel(self.groupBox)
        self.label_2.setGeometry(QtCore.QRect(10, 80, 71, 41))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.pushButton_start_2 = QtWidgets.QPushButton(self.groupBox)
        self.pushButton_start_2.setGeometry(QtCore.QRect(290, 20, 91, 41))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.pushButton_start_2.setFont(font)
        self.pushButton_start_2.setObjectName("pushButton_start_2")
        self.pushButton_close = QtWidgets.QPushButton(self.groupBox)
        self.pushButton_close.setGeometry(QtCore.QRect(490, 80, 101, 41))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.pushButton_close.setFont(font)
        self.pushButton_close.setObjectName("pushButton_close")
        self.pushButton_get_ip = QtWidgets.QPushButton(self.groupBox)
        self.pushButton_get_ip.setGeometry(QtCore.QRect(490, 20, 101, 41))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.pushButton_get_ip.setFont(font)
        self.pushButton_get_ip.setObjectName("pushButton_get_ip")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1020, 29))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "局域网视频通信程序"))
        self.label_3.setText(_translate("MainWindow", "接收视频/广播桌面"))
        self.label_4.setText(_translate("MainWindow", "本地视频/广播用户"))
        self.groupBox.setTitle(_translate("MainWindow", "功能"))
        self.pushButton_start_4.setText(_translate("MainWindow", "用户广播"))
        self.pushButton_end.setText(_translate("MainWindow", "结束程序"))
        self.lineEdit_ip.setText(_translate("MainWindow", "127.0.0.1"))
        self.lineEdit_broadcast.setText(_translate("MainWindow", "192.168.31.255"))
        self.pushButton_start.setText(_translate("MainWindow", "桌面广播"))
        self.label.setText(_translate("MainWindow", "目标IP："))
        self.pushButton_start_3.setText(_translate("MainWindow", "接收广播"))
        self.label_2.setText(_translate("MainWindow", "广播IP："))
        self.pushButton_start_2.setText(_translate("MainWindow", "视频聊天"))
        self.pushButton_close.setText(_translate("MainWindow", "关闭连接"))
        self.pushButton_get_ip.setText(_translate("MainWindow", "设置广播"))
