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
from PyQt5.QtWidgets import QDialog, QMainWindow, QVBoxLayout, QWidget, QHeaderView, QGridLayout, QTableWidgetItem, \
    QLabel, QMessageBox, QApplication
import global_vars
from component.notification import NotificationManager
from entity.Grade import Grade
from python_ui.messagebox import AutoCloseMessageBox
from service.experimentservice import ExperimentService
from service.paradigmservice import ParadigmService


class Window5(QWidget):
    toWindow4_signal = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__()
        uic.loadUi('./ui/infoView.ui', self)
        self.resize(1920, 1080)
        self.move(0, 0)
        self.groupBox.move(150, 134)
        self.setWindowFlags(Qt.FramelessWindowHint)

        self.experimentService = ExperimentService()
        self.experimentService.experiment_create_finish.connect(self.beginParadigm)
        # 绑定按钮事件
        self.backBtn.clicked.connect(self.backWindowFunction)
        # 表单事件
        self.nameEdit.textChanged.connect(self.nameEditFinish)
        self.collegeEdit.textChanged.connect(self.collegeEditFinish)
        self.ethnicEdit.textChanged.connect(self.ethnicEditFinish)
        self.ageEdit.valueChanged.connect(self.ageEditFinish)
        self.gradeEdit.currentIndexChanged.connect(self.gradeEditFinish)
        self.sex_0.toggled.connect(self.on_radio_btn_toggled)
        self.sex_1.toggled.connect(self.on_radio_btn_toggled)
        self.beginBtn.clicked.connect(self.beginExperiment)

        # 设置 表格 列宽为平均宽度
        self.set_table_column_widths()

        # 必要对象
        self.paradigmService = ParadigmService()

    # 开始运行范式
    def beginParadigm(self):
        flag = self.paradigmService.startParadigm()
        if flag:
            # 范式开始运行
            # 开始实验
            NotificationManager.show_notification(
                self,
                title="提示",
                message="范式运行成功,开始实验，请不要进行其他操作，等待范式运行结束",
                auto_close=True,
                timeout=3000
            )
            self.experimentService.beginExperiment()


    def beginExperiment(self):
        # 开始实验
        # 检查信息是否填写完整，设备是否正常连接，范式是否选择
        # 获取对象的所有属性和值
        # 创建并显示自动关闭的消息框

        attributes = vars(global_vars.student)
        # 遍历所有属性和值，检查是否有空值
        noneflag = False
        for key, value in attributes.items():
            if value in [None, '', [], {}, ()]:
                noneflag = True

        if noneflag:
            NotificationManager.show_notification(
                self,
                title="提示",
                message="被试者信息未填写完整",
                auto_close=True,
                timeout=3000
            )
        # 判断设备是否正常连接
        deviceflag = False
        # TODO 暂时未做
        # 范式是否选择
        paradigmflag = False
        if global_vars.paradigm_id is None:
            paradigmflag = True
        if paradigmflag:
            NotificationManager.show_notification(
                self,
                title="提示",
                message="范式未选择",
                auto_close=True,
                timeout=3000
            )

        # 确定选择的范式
        flag_select = self.paradigmService.selectParadigmById()
        if not flag_select:
            NotificationManager.show_notification(
                self,
                title="警告",
                message="范式选择出现错误,可能因本地无该范式文件",
                auto_close=True,
                timeout=3000
            )
        # 如果都正确完成了，则进行实验
        if not noneflag and not deviceflag and not paradigmflag:
            NotificationManager.show_notification(
                self,
                title="提示",
                message="实验开始,请不要进行其他操作，等待范式运行",
                auto_close=True,
                timeout=3000
            )
            print(global_vars.student)
            self.beginBtn.setEnabled(False)
            # 获取当前的焦点控件并清除其焦点
            current_focus_widget = QApplication.focusWidget()
            if current_focus_widget is not None:
                current_focus_widget.clearFocus()
            self.experimentService.createExperiment()

    # 初始化设备表格信息
    def initDeviceInfoTable(self):
        pass

    # 初始化范式表格信息
    def initParadigmInfoTable(self):
        if global_vars.paradigm_id is not None:
            # 根据id查询范式信息
            data = self.paradigmService.getParadigmById(global_vars.paradigm_id)
            print(data)
            # 清空表格内容
            self.paradigmTable.setRowCount(0)

            # 添加新数据
            self.paradigmTable.setRowCount(1)

            # 设置ID
            id_item = QTableWidgetItem(data['id'])
            id_item.setFlags(id_item.flags() & ~Qt.ItemIsEditable)  # 设置不可编辑
            self.paradigmTable.setItem(0, 0, id_item)

            # 设置名称
            name_item = QTableWidgetItem(data['name'])
            name_item.setFlags(name_item.flags() & ~Qt.ItemIsEditable)  # 设置不可编辑
            self.paradigmTable.setItem(0, 1, name_item)

            if data.get('description') == None:
                description = ""
            else:
                description = data.get('description')
            description_item = QTableWidgetItem(description)
            description_item.setFlags(description_item.flags() & ~Qt.ItemIsEditable)  # 设置不可编辑
            self.paradigmTable.setItem(0, 2, description_item)

            # 设置创建时间
            create_time_item = QTableWidgetItem(data['createTime'])
            create_time_item.setFlags(create_time_item.flags() & ~Qt.ItemIsEditable)  # 设置不可编辑
            self.paradigmTable.setItem(0, 3, create_time_item)
        else:
            # 清空表格
            self.paradigmTable.setRowCount(0)


    def set_table_column_widths(self):
        header = self.deviceTable.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.Stretch)
        header2 = self.paradigmTable.horizontalHeader()
        header2.setSectionResizeMode(QHeaderView.Stretch)
    # 名字输入完成
    def nameEditFinish(self):
        global_vars.student.name = self.nameEdit.text()

    # 学院输入完成
    def collegeEditFinish(self):
        global_vars.student.college = self.collegeEdit.text()

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
            if sender.text() == '男':
                global_vars.student.gender = 0
            else:
                global_vars.student.gender = 1


    # 初始化被试者信息
    def initUserInfo(self):
        print("初始化被试信息")
        self.nameEdit.setText(global_vars.student.name)
        self.collegeEdit.setText(global_vars.student.college)
        self.ethnicEdit.setText(global_vars.student.ethnic)
        self.ageEdit.setValue(global_vars.student.age)
        # 更新下拉列表
        grade = Grade()
        for item in grade.gradeList:
            self.gradeEdit.addItem(item)

        self.gradeEdit.setCurrentIndex(global_vars.student.grade)
        if global_vars.student.gender == '0':
            self.sex_0.setChecked(True)
        else:
            self.sex_1.setChecked(True)

    def backWindowFunction(self):
        self.toWindow4_signal.emit()




