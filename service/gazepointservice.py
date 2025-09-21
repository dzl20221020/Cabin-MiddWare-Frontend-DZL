# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2024/4/17 14:51
# @Author : DZL
# @File : gazepointservice.py
# @Software: PyCharm
import requests
from PyQt5.QtCore import QThread, pyqtSignal

import global_vars


class GazepointService(QThread):
    calibration_complete = pyqtSignal(bool)

    def __init__(self):
        super().__init__()
        self.calibraeFlag = False   # 是否校准的标志

    def run(self):
        self.calibrae()

    # 校准函数
    def calibrae(self):
        # 定义接口的 URL
        url = global_vars.SERVER_ADDRESS + "device/gazepoint/calibrae"

        # 定义要发送的数据（如果有的话）
        payload = {
            # 这里添加你需要发送的数据，如果有的话
        }

        # 发送 POST 请求
        try:
            response = requests.get(url, json=payload)
        except Exception as e:
            print(repr(e))

        # 检查响应状态码
        if response.status_code == 200:
            print("Calibration successful")
            self.calibration_complete.emit(True)
        else:
            print("Calibration failed")
            self.calibration_complete.emit(False)