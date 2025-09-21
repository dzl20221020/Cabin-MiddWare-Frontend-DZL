# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2024/4/17 14:14
# @Author : Lida
# @File : Window3.py
# @Software: PyCharm
# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2024/4/16 14:40
# @Author : DZL
# @File : Window2.py
# @Software: PyCharm
import json
import sys
import threading
from functools import partial


from PyQt5 import uic
from PyQt5.QtCore import Qt, QProcess, QEvent, QThread, pyqtSignal, QTimer
from PyQt5.QtWidgets import QDialog, QMainWindow, QVBoxLayout, QWidget, QHeaderView, QGridLayout

import global_vars
from python_ui.Card import CardWidget
from service.paradigmservice import ParadigmService


class Window4(QWidget):
    toWindow3_signal = pyqtSignal()
    toWindow5_signal = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__()
        uic.loadUi('./ui/paradigmView.ui', self)
        self.resize(1920, 1080)
        self.move(0, 0)
        self.groupBox.move(150, 134)
        self.setWindowFlags(Qt.FramelessWindowHint)

        # 必要对象
        self.paradigmService = ParadigmService()
        # 当前选中的卡片
        self.current_selected_card = None

        # 创建滚动内容的容器
        self.scroll_content = QWidget()
        self.scroll_layout = QVBoxLayout(self.scroll_content)

        # 创建卡片布局
        self.grid_layout = QGridLayout()

        # 绑定按钮事件
        self.backBtn.clicked.connect(self.backWindowFunction)
        self.nextBtn.clicked.connect(self.nextWindowFunction)



    def backWindowFunction(self):
        self.toWindow3_signal.emit()
    def nextWindowFunction(self):
        self.toWindow5_signal.emit()

    def cardSelect(self, card):
        if self.current_selected_card:
            self.current_selected_card.is_selected = False
            self.current_selected_card.update_style()

        card.is_selected = True
        card.update_style()
        global_vars.paradigm_id = card.id_text
        print("gloable_vars.paradigm_id:"+global_vars.paradigm_id)
        self.current_selected_card = card

    # 获取所有的范式信息
    def getAllParadigm(self):
        # 获取所有的范式信息
        paradigms = self.paradigmService.getAllParadigm()
        # 解析数据
        for index, paradigm in enumerate(paradigms):
            # 创建卡片
            card = CardWidget(paradigm.get("coverPath"), paradigm.get("id"), paradigm.get("name"),
                              paradigm.get("description"), paradigm.get("createTime"))
            # 添加卡片到布局
            row = index // 4  # 计算行号
            col = index % 4  # 计算列号
            self.grid_layout.addWidget(card, row, col)
            card.card_clicked.connect(partial(self.cardSelect, card))
            # 如果已经选中过，则初始化选中状态
            if global_vars.paradigm_id is not None and global_vars.paradigm_id == card.id_text:
                card.is_selected = True
                card.update_style()

        # 将卡片布局添加到滚动区域
        self.scroll_layout.addLayout(self.grid_layout)

        # 设置滚动区域的内容
        self.scroll_content.setLayout(self.scroll_layout)
        self.scrollArea.setWidget(self.scroll_content)



