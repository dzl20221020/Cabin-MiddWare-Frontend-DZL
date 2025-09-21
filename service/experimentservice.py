# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2024/4/17 14:51
# @Author : DZL
# @File : gazepointservice.py
# @Software: PyCharm
import requests
from PyQt5.QtCore import QThread, pyqtSignal

import global_vars


class ExperimentService(QThread):
    experiment_create_finish = pyqtSignal(bool)

    def __init__(self):
        super().__init__()

    def run(self):
        self.createExperiment()

    # 创建实验函数
    def createExperiment(self):
        # 定义接口的 URL
        url = global_vars.WORKSTATION_SERVER_ADDRESS + "/experiment/createExperiment"

        # 定义要发送的数据（如果有的话）
        payload = {
            "name":global_vars.student.name,
            "age":global_vars.student.age,
            "gender":global_vars.student.gender,
            "paradigmId":global_vars.paradigm_id,
            "userId":global_vars.student.userId
            # TODO 还有几个属性由于服务器也要改，所以暂时不动
        }

        # 发送 POST 请求
        try:
            response = requests.post(url, json=payload)
            print(response.json()["data"]["id"])
            global_vars.experiment_id = response.json()["data"]["id"]
        except Exception as e:
            print(repr(e))

        print(response)
        # 检查响应状态码
        if response.status_code == 200:
            print("create successful")
            self.experiment_create_finish.emit(True)
        else:
            print("create failed")
            self.experiment_create_finish.emit(False)

    def beginExperiment(self):
        # 定义接口的 URL
        url = global_vars.WORKSTATION_SERVER_ADDRESS + "/experiment/startExperiment/" + global_vars.experiment_id

        # 定义要发送的数据（如果有的话）
        payload = {
        }

        # 发送 POST 请求
        try:
            response = requests.get(url, json=payload)
        except Exception as e:
            print(repr(e))

        print(response)
        # 检查响应状态码
        if response.status_code == 200:
            print("begin successful")
        else:
            print("begin failed")
