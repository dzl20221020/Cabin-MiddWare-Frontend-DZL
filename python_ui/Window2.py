# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2024/4/16 14:40
# @Author : DZL
# @File : Window2.py
# @Software: PyCharm
import sys

from PyQt5 import uic
from PyQt5.QtCore import Qt, QProcess, QEvent, pyqtSignal
from PyQt5.QtWidgets import QDialog, QMainWindow, QWidget
from entity.Grade import Grade
import global_vars


class Window2(QWidget):
    toWindow1_signal = pyqtSignal()
    toWindow3_signal = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__()
        uic.loadUi('./ui/startWindow1.ui', self)
        self.resize(1920, 1080)
        self.move(0, 0)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.groupBox.move(560, 256)

        # 更新表单
        self.updateForm()

        # 按钮事件绑定
        self.indexBtn.clicked.connect(self.backIndex)
        self.nextBtn.clicked.connect(self.nextWindow)

        #表单事件
        self.nameEdit.textChanged .connect(self.nameEditFinish)
        self.collegeEdit.textChanged .connect(self.collegeEditFinish)
        self.numberEdit.textChanged .connect(self.numberEditFinish)
        self.ethnicEdit.textChanged .connect(self.ethnicEditFinish)
        self.ageEdit.valueChanged.connect(self.ageEditFinish)
        self.gradeEdit.currentIndexChanged.connect(self.gradeEditFinish)
        self.sex_0.toggled.connect(self.on_radio_btn_toggled)
        self.sex_1.toggled.connect(self.on_radio_btn_toggled)

    # 名字输入完成
    def nameEditFinish(self):
        global_vars.student.name = self.nameEdit.text()

    # 学院输入完成
    def collegeEditFinish(self):
        global_vars.student.college = self.collegeEdit.text()

    # 学生编号输入完成
    def numberEditFinish(self):
        global_vars.student.userId = self.numberEdit.text()

    # 民族输入完成
    def ethnicEditFinish(self):
        global_vars.student.ethnic = self.ethnicEdit.text()

    # 年龄输入完成
    def ageEditFinish(self):
        global_vars.student.age = self.ageEdit.value()

    # 年级输入完成
    def gradeEditFinish(self):
        global_vars.student.grade = self.gradeEdit.currentIndex()

    def on_radio_btn_toggled(self):
        sender = self.sender()
        if sender.isChecked():
            print(sender.text(), "被选中")
            print(sender.text() == '男')
            if sender.text() == '男':
                global_vars.student.gender = 0
            else:
                global_vars.student.gender = 1
            print(str(global_vars.student.__str__()))


    # 初始创建页面时更新表单
    def updateForm(self):
        self.nameEdit.setText(global_vars.student.name)
        self.collegeEdit.setText(global_vars.student.college)
        self.numberEdit.setText(global_vars.student.userId)
        self.ethnicEdit.setText(global_vars.student.ethnic)
        self.ageEdit.setValue(global_vars.student.age)
        if global_vars.student.gender == 0:
            self.sex_0.setChecked(True)
        else:
            self.sex_1.setChecked(True)

        # 更新下拉列表
        grade = Grade()
        for item in grade.gradeList:
            self.gradeEdit.addItem(item)

        self.gradeEdit.setCurrentIndex(global_vars.student.grade)

    # 返回首页
    def backIndex(self):
        self.toWindow1_signal.emit()

    def nextWindow(self):
        self.toWindow3_signal.emit()
