# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2024/4/16 14:27
# @Author : DZL
# @File : MainWindow.py
# @Software: PyCharm
from PyQt5 import uic
from PyQt5.QtCore import Qt, pyqtSignal, QTimer
from PyQt5.QtWidgets import QDialog, QMainWindow, QWidget

import global_vars
from component.notification import NotificationManager
from service.musicservice import MusicService


class Window1(QWidget):
    startExperiment_signal = pyqtSignal()  # 定义一个信号，用于让主界面切换页面

    def __init__(self, parent=None):
        super().__init__()
        uic.loadUi('./ui/window1.ui', self)
        self.resize(1920, 1080)
        self.move(0,0)
        self.setWindowFlags(Qt.FramelessWindowHint)

        # 初始化定时器
        self.init_check_timer = QTimer()
        self.init_check_timer.timeout.connect(self.checkInitializationStatus)
        self.init_check_timer.start(5000)  # 每隔5秒检查一次



        # 按钮点击事件
        self.startExp.clicked.connect(self.startExperiment)
        self.playmusic.clicked.connect(self.playMusic)

        # 必要对象
        self.musicService = MusicService()

    def playMusic(self):
        # 播放音乐
        self.musicService.playMusic()


    def startExperiment(self):
        # 通过实验状态进行判断，是否系统准备就绪
        if (global_vars.experiment_status == 'WAITING' or global_vars.experiment_status == None):
            # 进入开始实验流程
            # 进入实验者信息输入页面
            self.startExperiment_signal.emit()
        else:
            NotificationManager.show_notification(
                self,
                title="提示",
                message="检测到系统还未初始化完毕，请等待系统初始化",
                auto_close=True,
                timeout=10000
            )
            # 启动定时检查
            self.init_check_timer.start()
            self.startExp.setEnabled(False)

    def checkInitializationStatus(self):
        # 检查实验状态是否已经初始化完毕
        if global_vars.experiment_status is not None:
            self.init_check_timer.stop()  # 停止定时器
            NotificationManager.show_notification(
                self,
                title="提示",
                message="系统已初始化完毕，您可以开始实验",
                auto_close=True,
                timeout=5000
            )
            self.startExp.setEnabled(True)


