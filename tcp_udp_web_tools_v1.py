# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'tcp_tt.ui'
#
# Created by: PyQt5 UI code generator 5.10
#
# WARNING! All changes made in this file will be lost!

"""
v1.0计划：
整合TCP/UDP测试工具；
添加静态web服务器，用于响应浏览器；
"""

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QDialog, QMessageBox, QFileDialog
import sys
import socket
import threading
import ctypes
import inspect
import re


class Ui_TCP(QDialog):
    # 定义一个信号
    signal_write_msg = QtCore.pyqtSignal(str)

    def __init__(self, st):
        """
        初始化，定义变量
        :param st: StopThreading类创建的对象
        """
        super(Ui_TCP, self).__init__()

        self._translate = QtCore.QCoreApplication.translate
        self.st = st

        self.pushButton_get_ip = QtWidgets.QPushButton()
        self.pushButton_link = QtWidgets.QPushButton()
        self.pushButton_unlink = QtWidgets.QPushButton()
        self.pushButton_clear = QtWidgets.QPushButton()
        self.pushButton_exit = QtWidgets.QPushButton()
        self.pushButton_send = QtWidgets.QPushButton()
        self.pushButton_dir = QtWidgets.QPushButton()
        self.label_port = QtWidgets.QLabel()
        self.label_ip = QtWidgets.QLabel()
        self.label_rev = QtWidgets.QLabel()
        self.label_send = QtWidgets.QLabel()
        self.label_sendto = QtWidgets.QLabel()
        self.label_dir = QtWidgets.QLabel()
        self.label_written = QtWidgets.QLabel()
        self.textEdit_send = QtWidgets.QTextEdit()
        self.textEdit_ip_send = QtWidgets.QTextEdit()
        self.textEdit_port = QtWidgets.QTextEdit()
        self.textBrowser_recv = QtWidgets.QTextBrowser()
        self.textBrowser_ip_local = QtWidgets.QTextBrowser()
        self.comboBox_tcp = QtWidgets.QComboBox()

        self.msg = None
        self.port = None
        self.address = None
        self.dir = None
        self.msg_dir = None
        self.link = False
        self.sever_th = None
        self.client_th = None
        self.client_socket = None
        self.client_address = None
        self.web_client_socket = None
        self.client_socket_list = list()

        # 创建TCP/UDP套接字
        self.tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        # 将TCP套接字四次挥手后的TIME_WAIT状态取消
        self.tcp_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    def ui_setup(self, t_c_p):
        """
        控件属性的设置
        :param t_c_p: QDialog类创建的对象
        :return: None
        """
        t_c_p.setObjectName("t_c_p")
        t_c_p.resize(640, 480)
        t_c_p.setAcceptDrops(False)
        t_c_p.setSizeGripEnabled(False)
        # 使用socket模块获取本机ip
        my_addr = socket.gethostbyname(socket.gethostname())

        self.pushButton_get_ip = QtWidgets.QPushButton(t_c_p)
        self.pushButton_link = QtWidgets.QPushButton(t_c_p)
        self.pushButton_unlink = QtWidgets.QPushButton(t_c_p)
        self.pushButton_clear = QtWidgets.QPushButton(t_c_p)
        self.pushButton_exit = QtWidgets.QPushButton(t_c_p)
        self.pushButton_send = QtWidgets.QPushButton(t_c_p)
        self.pushButton_dir = QtWidgets.QPushButton(t_c_p)
        self.label_port = QtWidgets.QLabel(t_c_p)
        self.label_ip = QtWidgets.QLabel(t_c_p)
        self.label_rev = QtWidgets.QLabel(t_c_p)
        self.label_send = QtWidgets.QLabel(t_c_p)
        self.label_sendto = QtWidgets.QLabel(t_c_p)
        self.label_dir = QtWidgets.QLabel(t_c_p)
        self.label_written = QtWidgets.QLabel(t_c_p)
        self.textEdit_send = QtWidgets.QTextEdit(t_c_p)
        self.textEdit_ip_send = QtWidgets.QTextEdit(t_c_p)
        self.textEdit_port = QtWidgets.QTextEdit(t_c_p)
        self.textBrowser_recv = QtWidgets.QTextBrowser(t_c_p)
        self.textBrowser_ip_local = QtWidgets.QTextBrowser(t_c_p)
        self.comboBox_tcp = QtWidgets.QComboBox(t_c_p)

        font = QtGui.QFont()
        font.setFamily("Yuppy TC")
        font.setPointSize(20)
        font.setBold(True)
        font.setItalic(False)
        font.setUnderline(True)
        font.setWeight(75)
        font.setStrikeOut(False)

        self.label_rev.setGeometry(QtCore.QRect(410, 20, 80, 30))
        self.label_rev.setFont(font)
        self.label_rev.setObjectName("label_rev")

        self.label_send.setGeometry(QtCore.QRect(100, 160, 80, 30))
        self.label_send.setFont(font)
        self.label_send.setObjectName("label_send")

        self.label_ip.setGeometry(QtCore.QRect(20, 20, 50, 20))
        self.label_ip.setObjectName("label_ip")

        self.label_written.setGeometry(QtCore.QRect(40, 380, 120, 20))
        self.label_written.setObjectName("label_written")

        self.label_sendto.hide()
        self.label_sendto.setGeometry(QtCore.QRect(20, 70, 50, 20))
        self.label_sendto.setObjectName("label_sendto")

        self.label_port.setGeometry(QtCore.QRect(20, 45, 60, 20))
        self.label_port.setObjectName("label_port")

        self.label_dir.hide()
        self.label_dir.setWordWrap(True)
        self.label_dir.setGeometry(QtCore.QRect(20, 240, 260, 80))
        self.label_dir.setObjectName("label_dir")

        self.comboBox_tcp.setGeometry(QtCore.QRect(10, 110, 100, 28))
        self.comboBox_tcp.setObjectName("comboBox_tcp")
        self.comboBox_tcp.addItem("")
        self.comboBox_tcp.addItem("")
        self.comboBox_tcp.addItem("")
        self.comboBox_tcp.addItem("")
        self.comboBox_tcp.addItem("")

        self.pushButton_link.setGeometry(QtCore.QRect(110, 110, 100, 32))
        self.pushButton_link.setObjectName("pushButton_link")

        self.pushButton_unlink.setEnabled(False)
        self.pushButton_unlink.setGeometry(QtCore.QRect(200, 110, 100, 32))
        self.pushButton_unlink.setObjectName("pushButton_unlink")

        self.pushButton_get_ip.setGeometry(QtCore.QRect(190, 15, 100, 32))
        self.pushButton_get_ip.setObjectName("pushButton_get_ip")

        self.pushButton_send.setGeometry(QtCore.QRect(170, 370, 113, 32))
        self.pushButton_send.setObjectName("pushButton_send")

        self.pushButton_exit.setGeometry(QtCore.QRect(170, 410, 113, 32))
        self.pushButton_exit.setObjectName("pushButton_exit")

        self.pushButton_clear.setGeometry(QtCore.QRect(500, 20, 113, 32))
        self.pushButton_clear.setObjectName("pushButton_clear")

        self.pushButton_dir.hide()
        self.pushButton_dir.setGeometry(QtCore.QRect(20, 200, 113, 32))
        self.pushButton_dir.setObjectName("pushButton_dir")

        self.textEdit_port.setGeometry(QtCore.QRect(70, 45, 55, 20))
        self.textEdit_port.setObjectName("textEdit_port")

        self.textEdit_send.setGeometry(QtCore.QRect(30, 200, 250, 150))
        self.textEdit_send.setObjectName("textEdit_send")

        self.textEdit_ip_send.hide()
        self.textEdit_ip_send.setGeometry(QtCore.QRect(70, 70, 120, 20))
        self.textEdit_ip_send.setObjectName("textEdit_ip_send")

        self.textBrowser_recv.setGeometry(QtCore.QRect(300, 60, 320, 400))
        self.textBrowser_recv.setObjectName("textBrowser_recv")

        self.textBrowser_ip_local.setGeometry(QtCore.QRect(70, 20, 120, 20))
        self.textBrowser_ip_local.setObjectName("textBrowser_ip_local")
        self.textBrowser_ip_local.insertPlainText(str(my_addr))

        self.connect(t_c_p)
        self.ui_translate(t_c_p)
        QtCore.QMetaObject.connectSlotsByName(t_c_p)

    def ui_translate(self, t_c_p):
        """
        控件默认显示文字的设置
        :param t_c_p: QDialog类创建的对象
        :return: None
        """
        t_c_p.setWindowTitle(self._translate("t_c_p", "TCP网络测试工具"))
        self.comboBox_tcp.setItemText(0, self._translate("t_c_p", "TCP服务端"))
        self.comboBox_tcp.setItemText(1, self._translate("t_c_p", "TCP客户端"))
        self.comboBox_tcp.setItemText(2, self._translate("t_c_p", "UDP服务端"))
        self.comboBox_tcp.setItemText(3, self._translate("t_c_p", "UDP客户端"))
        self.comboBox_tcp.setItemText(4, self._translate("t_c_p", "WEB服务端"))
        self.pushButton_link.setText(self._translate("t_c_p", "连接网络"))
        self.pushButton_unlink.setText(self._translate("t_c_p", "断开网络"))
        self.pushButton_get_ip.setText(self._translate("t_c_p", "重新获取IP"))
        self.pushButton_clear.setText(self._translate("t_c_p", "清除消息"))
        self.pushButton_send.setText(self._translate("t_c_p", "发送"))
        self.pushButton_exit.setText(self._translate("t_c_p", "退出系统"))
        self.pushButton_dir.setText(self._translate("t_c_p", "选择路径"))
        self.label_ip.setText(self._translate("t_c_p", "本机IP:"))
        self.label_port.setText(self._translate("t_c_p", "端口号:"))
        self.label_sendto.setText(self._translate("t_c_p", "目标IP:"))
        self.label_rev.setText(self._translate("t_c_p", "接收区域"))
        self.label_send.setText(self._translate("t_c_p", "发送区域"))
        self.label_dir.setText(self._translate("t_c_p", "请选择index.html所在的文件夹"))
        self.label_written.setText(self._translate("t_c_p", "Written by LiDuo"))

    def connect(self, t_c_p):
        """
        控件信号-槽的设置
        :param t_c_p: QDialog类创建的对象
        :return: None
        """
        self.signal_write_msg.connect(self.write_msg)
        self.comboBox_tcp.currentIndexChanged.connect(self.combobox_change)
        self.pushButton_link.clicked.connect(self.click_link)
        self.pushButton_unlink.clicked.connect(self.click_unlink)
        self.pushButton_get_ip.clicked.connect(self.click_get_ip)
        self.pushButton_clear.clicked.connect(self.click_clear)
        self.pushButton_send.clicked.connect(self.all_send)
        self.pushButton_dir.clicked.connect(self.click_dir)
        self.pushButton_exit.clicked.connect(t_c_p.close)

    def combobox_change(self):
        """
        combobox控件内容改变时触发的槽
        :return: None
        """
        self.close_all()
        if self.comboBox_tcp.currentIndex() == 0 or self.comboBox_tcp.currentIndex() == 2:
            self.label_sendto.hide()
            self.textEdit_ip_send.hide()
            self.textEdit_send.show()
            self.label_dir.hide()
            self.pushButton_dir.hide()
            self.pushButton_send.show()
            self.textEdit_port.setGeometry(QtCore.QRect(70, 45, 55, 20))
            self.label_port.setText(self._translate("t_c_p", "端口号:"))
        if self.comboBox_tcp.currentIndex() == 1 or self.comboBox_tcp.currentIndex() == 3:
            self.label_sendto.show()
            self.textEdit_ip_send.show()
            self.textEdit_send.show()
            self.label_dir.hide()
            self.pushButton_dir.hide()
            self.pushButton_send.show()
            self.textEdit_port.setGeometry(QtCore.QRect(80, 45, 55, 20))
            self.label_port.setText(self._translate("t_c_p", "目标端口:"))
        if self.comboBox_tcp.currentIndex() == 4:
            self.label_sendto.hide()
            self.textEdit_ip_send.hide()
            self.textEdit_send.hide()
            self.label_dir.show()
            self.pushButton_dir.show()
            self.pushButton_send.hide()
            self.textEdit_port.setGeometry(QtCore.QRect(70, 45, 55, 20))
            self.label_port.setText(self._translate("t_c_p", "端口号:"))

    def click_link(self):
        """
        pushbutton_link控件点击触发的槽
        :return: None
        """
        if self.comboBox_tcp.currentIndex() == 0:
            self.tcp_server_start()
        if self.comboBox_tcp.currentIndex() == 1:
            self.tcp_client_start()
        if self.comboBox_tcp.currentIndex() == 2:
            self.udp_server_start()
        if self.comboBox_tcp.currentIndex() == 3:
            self.udp_client_start()
        if self.comboBox_tcp.currentIndex() == 4:
            self.web_server_start()
        self.link = True
        self.pushButton_unlink.setEnabled(True)
        self.pushButton_link.setEnabled(False)

    def click_unlink(self):
        """
        pushbutton_unlink控件点击触发的槽
        :return: None
        """
        self.close_all()
        self.link = False
        self.pushButton_unlink.setEnabled(False)
        self.pushButton_link.setEnabled(True)

    def click_get_ip(self):
        """
        pushbutton_get_ip控件点击触发的槽
        :return: None
        """
        self.textBrowser_ip_local.clear()
        my_addr = socket.gethostbyname(socket.gethostname())
        self.textBrowser_ip_local.insertPlainText(str(my_addr))

    def click_clear(self):
        """
        pushbutton_clear控件点击触发的槽
        :return: None
        """
        self.textBrowser_recv.clear()

    def click_dir(self):
        self.dir = QFileDialog.getExistingDirectory(self, "获取文件夹路径", './')
        if self.dir:
            self.label_dir.setText(self._translate("t_c_p", "%s" % self.dir))

    def close_all(self):
        """
        功能函数，关闭网络连接的方法
        :return:
        """
        if self.comboBox_tcp.currentIndex() == 0:
            try:
                for client, address in self.client_socket_list:
                    client.close()
                self.tcp_socket.close()
                if self.link is True:
                    self.msg = '已断开网络\n'
                    self.signal_write_msg.emit("写入")

                self.st.stop_thread(self.sever_th)
            except Exception as ret:
                pass
        if self.comboBox_tcp.currentIndex() == 1:
            try:
                self.tcp_socket.close()
                if self.link is True:
                    self.msg = '已断开网络\n'
                    self.signal_write_msg.emit("写入")

                self.st.stop_thread(self.sever_th)
                self.st.stop_thread(self.client_th)
            except Exception as ret:
                pass
        if self.comboBox_tcp.currentIndex() == 2:
            try:
                self.udp_socket.close()
                if self.link is True:
                    self.msg = '已断开网络\n'
                    self.signal_write_msg.emit("写入")

                self.st.stop_thread(self.sever_th)
                self.st.stop_thread(self.client_th)
            except Exception as ret:
                pass
        if self.comboBox_tcp.currentIndex() == 3:
            try:
                self.udp_socket.close()
                if self.link is True:
                    self.msg = '已断开网络\n'
                    self.signal_write_msg.emit("写入")

                self.st.stop_thread(self.sever_th)
                self.st.stop_thread(self.client_th)
            except Exception as ret:
                pass
        if self.comboBox_tcp.currentIndex() == 4:
            try:
                for client, address in self.client_socket_list:
                    client.close()
                self.tcp_socket.close()
                if self.link is True:
                    self.msg = '已断开网络\n'
                    self.signal_write_msg.emit("写入")

                self.st.stop_thread(self.sever_th)
                self.st.stop_thread(self.client_th)
            except Exception as ret:
                pass
        self.reset()

    def tcp_server_start(self):
        """
        功能函数，TCP服务端开启的方法
        :return: None
        """
        self.tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.tcp_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.tcp_socket.setblocking(False)
        try:
            self.port = int(self.textEdit_port.toPlainText())
            self.tcp_socket.bind(('', self.port))
        except Exception as ret:
            self.msg = '请检查端口号\n'
            self.signal_write_msg.emit("写入")
        else:
            self.tcp_socket.listen()
            self.sever_th = threading.Thread(target=self.tcp_server_concurrency)
            self.sever_th.start()
            self.msg = 'TCP服务端正在监听端口:%s\n' % str(self.port)
            self.signal_write_msg.emit("写入")

    def tcp_server_concurrency(self):
        """
        功能函数，供创建线程的方法；
        使用子线程用于监听并创建连接，使主线程可以继续运行，以免无响应
        使用非阻塞式并发用于接收客户端消息，减少系统资源浪费，使软件轻量化
        :return:None
        """
        while True:
            try:
                self.client_socket, self.client_address = self.tcp_socket.accept()
            except Exception as ret:
                pass
            else:
                self.client_socket.setblocking(False)
                # 将创建的客户端套接字存入列表
                self.client_socket_list.append((self.client_socket, self.client_address))
                self.msg = 'TCP服务端已连接IP:%s端口:%s\n' % self.client_address
                self.signal_write_msg.emit("写入")
            # 轮询客户端套接字列表，接收数据
            for client, address in self.client_socket_list:
                try:
                    recv_msg = client.recv(1024)
                except Exception as ret:
                    pass
                else:
                    if recv_msg:
                        msg = recv_msg.decode('utf-8')
                        self.msg = '来自IP:{}端口:{}:\n{}\n'.format(address[0], address[1], msg)
                        self.signal_write_msg.emit("写入")
                    else:
                        client.close()
                        self.client_socket_list.remove((client, address))

    def tcp_client_start(self):
        """
        功能函数，TCP客户端连接其他服务端的方法
        :return:
        """
        self.tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.tcp_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        try:
            self.address = (str(self.textEdit_ip_send.toPlainText()), int(self.textEdit_port.toPlainText()))
        except Exception as ret:
            self.msg = '请检查目标IP，目标端口\n'
            self.signal_write_msg.emit("写入")
        else:
            try:
                self.msg = '正在连接目标服务器\n'
                self.signal_write_msg.emit("写入")
                self.tcp_socket.connect(self.address)
            except Exception as ret:
                self.msg = '无法连接目标服务器\n'
                self.signal_write_msg.emit("写入")
            else:
                self.client_th = threading.Thread(target=self.tcp_client_concurrency)
                self.client_th.start()
                self.msg = 'TCP客户端已连接IP:%s端口:%s\n' % self.address
                self.signal_write_msg.emit("写入")

    def tcp_client_concurrency(self):
        """
        功能函数，用于TCP客户端创建子线程的方法，阻塞式接收
        :return:
        """
        while True:
            recv_msg = self.tcp_socket.recv(1024)
            if recv_msg:
                msg = recv_msg.decode('utf-8')
                self.msg = '来自IP:{}端口:{}:\n{}\n'.format(self.address[0], self.address[1], msg)
                self.signal_write_msg.emit("写入")
            else:
                self.tcp_socket.close()
                self.reset()
                self.msg = '从服务器断开连接\n'
                self.signal_write_msg.emit("写入")
                break

    def udp_server_start(self):
        self.udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            self.port = int(self.textEdit_port.toPlainText())
            address = ('', self.port)
            self.udp_socket.bind(address)
        except Exception as ret:
            self.msg = '请检查端口号\n'
            self.signal_write_msg.emit("写入")
        else:
            self.sever_th = threading.Thread(target=self.udp_server_concurrency)
            self.sever_th.start()
            self.msg = 'UDP服务端正在监听端口:{}\n'.format(self.port)
            self.signal_write_msg.emit("写入")

    def udp_server_concurrency(self):
        while True:
            recv_msg, recv_addr = self.udp_socket.recvfrom(1024)
            msg = recv_msg.decode('utf-8')
            self.msg = '来自IP:{}端口:{}:\n{}\n'.format(recv_addr[0], recv_addr[1], msg)
            self.signal_write_msg.emit("写入")

    def udp_client_start(self):
        self.udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            self.address = (str(self.textEdit_ip_send.toPlainText()), int(self.textEdit_port.toPlainText()))
        except Exception as ret:
            self.msg = '请检查目标IP，目标端口\n'
            self.signal_write_msg.emit("写入")
        else:
            self.msg = 'UDP客户端已启动\n'
            self.signal_write_msg.emit("写入")

    def web_server_start(self):
        """
        功能函数，WEB服务端开启的方法
        :return: None
        """
        self.tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.tcp_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        # 设置为非阻塞式
        self.tcp_socket.setblocking(False)
        try:
            self.port = int(self.textEdit_port.toPlainText())
            self.tcp_socket.bind(('', self.port))
        except Exception as ret:
            self.msg = '请检查端口号\n'
            self.signal_write_msg.emit("写入")
        else:
            self.tcp_socket.listen()
            self.sever_th = threading.Thread(target=self.web_server_concurrency)
            self.sever_th.start()
            self.msg = 'WEB服务端正在监听端口:%s\n' % str(self.port)
            self.signal_write_msg.emit("写入")

    def web_server_concurrency(self):
        """
        功能函数，供创建线程的方法；
        使用子线程用于监听并创建连接，使主线程可以继续运行，以免无响应
        使用非阻塞式并发用于接收客户端消息，减少系统资源浪费，使软件轻量化
        :return:None
        """
        while True:
            try:
                self.client_socket, self.client_address = self.tcp_socket.accept()
            except Exception as ret:
                pass
            else:
                self.client_socket.setblocking(False)
                # 将创建的客户端套接字存入列表
                self.client_socket_list.append((self.client_socket, self.client_address))
                self.msg = 'WEB服务端已连接浏览器，IP:%s端口:%s\n' % self.client_address
                self.signal_write_msg.emit("写入")
            # 轮询客户端套接字列表，接收数据
            for client, address in self.client_socket_list:
                try:
                    recv_msg = client.recv(1024)
                except Exception as ret:
                    pass
                else:
                    if recv_msg:
                        msg = recv_msg.decode('utf-8')
                        msg_lines = msg.splitlines()
                        msg_dir = re.match(r"[^/]+(/[^ ]*)", msg_lines[0])
                        self.msg_dir = msg_dir.group(1)
                        self.msg = '来自IP:{}端口:{}:\n请求路径:{}\n'.format(address[0], address[1], self.msg_dir)
                        self.signal_write_msg.emit("写入")
                        self.web_client_socket = client
                        self.all_send()
                    else:
                        client.close()
                        self.client_socket_list.remove((client, address))

    def all_send(self):
        """
        功能函数，用于TCP服务端和TCP/UDP客户端发送消息
        :return: None
        """
        if self.link is False:
            self.msg = '请选择服务，并点击连接网络\n'
            self.signal_write_msg.emit("写入")
        else:
            try:
                send_msg = (str(self.textEdit_send.toPlainText())).encode('utf-8')
                if self.comboBox_tcp.currentIndex() == 0:
                    for client, address in self.client_socket_list:
                        client.send(send_msg)
                    self.msg = 'TCP服务端已发送\n'
                    self.signal_write_msg.emit("写入")
                if self.comboBox_tcp.currentIndex() == 1:
                    self.tcp_socket.send(send_msg)
                    self.msg = 'TCP客户端已发送\n'
                    self.signal_write_msg.emit("写入")
                if self.comboBox_tcp.currentIndex() == 2:
                    self.msg = 'UDP服务端无法发送，请切换为UDP客户端\n'
                    self.signal_write_msg.emit("写入")
                if self.comboBox_tcp.currentIndex() == 3:
                    self.udp_socket.sendto(send_msg, self.address)
                    self.msg = 'UDP客户端已发送\n'
                    self.signal_write_msg.emit("写入")
                if self.comboBox_tcp.currentIndex() == 4:
                    header, body = self.web_send_msg()
                    self.web_client_socket.send(header)
                    self.web_client_socket.send(body)
                    self.msg = 'WEB服务端已回复\n'
                    self.signal_write_msg.emit("写入")
            except Exception as ret:
                print(ret)
                self.msg = '发送失败\n'
                self.signal_write_msg.emit("写入")

    def web_send_msg(self):
        if str(self.msg_dir) == '/':
            self.msg_dir = '/index.html'
            dir = str(self.dir) + str(self.msg_dir)
        else:
            dir = str(self.dir) + str(self.msg_dir)
        try:
            file_type = re.match(r'[^.]+\.(.*)$', self.msg_dir)
            file_type = file_type.group(1)
            if file_type == 'png':
                file_header = 'Content-Type: image/%s; charset=utf-8\r\n' % file_type
            elif file_type == 'css' or file_type == 'html':
                file_header = 'Content-Type: text/%s; charset=utf-8\r\n' % file_type
            else:
                file_header = 'Content-Type: text/html; charset=utf-8\r\n'
        except Exception as ret:
            file_header = 'Content-Type: text/html; charset=utf-8\r\n'

        try:
            f = open(dir, 'rb')
        except Exception as ret:
            file = '你要的东西不见了'.encode('utf-8')
            response_header = ('HTTP/1.1 404 NOT FOUND\r\n' +
                               'Connection: Keep-Alive\r\n' +
                               'Content-Length: %d\r\n' % len(file) +
                               file_header +
                               '\r\n')
        else:
            file = f.read()
            f.close()
            response_header = ('HTTP/1.1 200 OK\r\n' +
                               'Connection: Keep-Alive\r\n' +
                               'Content-Length: %d\r\n' % len(file) +
                               file_header +
                               '\r\n')
        response_body = file

        return response_header.encode('utf-8'), response_body

    def write_msg(self):
        """
        功能函数，向接收区写入数据的方法
        信号-槽触发
        tip：PyQt程序的子线程中，使用非规定的语句向主线程的界面传输字符是不允许的
        :return: None
        """
        self.textBrowser_recv.insertPlainText(self.msg)

    def reset(self):
        """
        功能函数，将按钮重置为初始状态
        :return:None
        """
        self.link = False
        self.client_socket_list = list()
        self.pushButton_unlink.setEnabled(False)
        self.pushButton_link.setEnabled(True)


class Dialog(QDialog):
    """对QDialog类重写，实现一些功能"""

    def __init__(self, ui):
        super(Dialog, self).__init__()
        self.ui = ui

    def closeEvent(self, event):
        """
        重写closeEvent方法，实现dialog窗体关闭时执行一些代码
        :param event: close()触发的事件
        :return: None
        """
        reply = QMessageBox.question(self,
                                     'TCP/UDP网络测试助手',
                                     "是否要退出TCP/UDP网络测试助手？",
                                     QMessageBox.Yes | QMessageBox.No,
                                     QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.ui.close_all()
            event.accept()
        else:
            event.ignore()


class StopThreading:
    """强制关闭线程的方法"""

    @staticmethod
    def _async_raise(tid, exc_type):
        tid = ctypes.c_long(tid)
        if not inspect.isclass(exc_type):
            exc_type = type(exc_type)
        res = ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, ctypes.py_object(exc_type))
        if res == 0:
            raise ValueError("invalid thread id")
        elif res != 1:
            ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, None)
            raise SystemError("PyThreadState_SetAsyncExc failed")

    def stop_thread(self, thread):
        self._async_raise(thread.ident, SystemExit)


def main():
    """
    主函数，用于运行程序
    :return: None
    """
    app = QApplication(sys.argv)
    st = StopThreading()
    ui = Ui_TCP(st)
    dialog = Dialog(ui)
    ui.ui_setup(dialog)
    dialog.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
