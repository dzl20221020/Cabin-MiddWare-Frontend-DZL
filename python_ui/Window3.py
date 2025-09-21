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
import ast
import re

import threading
import time

import websocket

from PyQt5 import uic
from PyQt5.QtCore import Qt, QProcess, QEvent, QThread, pyqtSignal, QTimer
from PyQt5.QtWidgets import QDialog, QMainWindow, QVBoxLayout, QWidget, QHeaderView, QTableWidgetItem, QTableWidget

from service.gazepointservice import GazepointService


# class WebSocketClient(QThread):
#     data_received = pyqtSignal(list)
#
#     def __init__(self):
#         super(WebSocketClient, self).__init__()
#         self.lock = threading.Lock()
#         self.ws = websocket.WebSocketApp("ws://localhost:8765",
#                                          on_message=self.on_message,
#                                          on_error=self.on_error,
#                                          on_close=self.on_close)
#         self.data_buffer = []
#         self.sample_rate = 50  # 降采样率，每隔多少个数据点取一个样本
#
#     def on_message(self, ws, message):
#         print(message)
#         # # 解析 JSON 数据
#         # parsed_data = json.loads(message)
#         #
#         # # 提取八通道数据
#         # eight_channel_data = parsed_data["data"]
#         # # 进行数据降采样
#         # # downsampled_data = self.downsample(eight_channel_data)
#         # # data = [float(val) for val in message.split(',')]
#         # self.data_buffer.append(eight_channel_data)
#
#     def downsample(self, data):
#         return [data[i] for i in range(0, len(data), self.sample_rate)]
#
#     def on_error(self, ws, error):
#         print("WebSocket error:", error)
#
#     def on_close(self, ws):
#         print("WebSocket closed")
#
#     def run(self):
#         self.ws.run_forever()

class WebSocketClient(QThread):
    data_received = pyqtSignal(str)

    def __init__(self):
        super(WebSocketClient, self).__init__()
        self.lock = threading.Lock()
        self.url = "ws://127.0.0.1:8888/websocket/w"
        self.ws = None

    def on_message(self, ws, message):
        print(message)
        self.data_received.emit(message)

    def on_error(self, ws, error):
        print("WebSocket error:", error)

    def on_close(self, ws, close_status_code, close_msg):
        print(f"WebSocket closed with code: {close_status_code}, message: {close_msg}")
        self.retry_connection()

    def on_open(self, ws):
        print("WebSocket connection opened")

    def send_data(self, data):
        with self.lock:
            if self.ws:
                self.ws.send(data)

    def connect(self):
        if self.ws:
            self.ws.close()  # 确保之前的连接已关闭

        self.ws = websocket.WebSocketApp(
            self.url,
            on_message=self.on_message,
            on_error=self.on_error,
            on_close=self.on_close
        )
        self.ws.on_open = self.on_open

        self.ws.run_forever()

    def retry_connection(self):
        self.connect()
        if self.connected:
            print("连接成功!")
        else:
            print("连接失败!")


    def run(self):
        self.retry_connection()
class Window3(QWidget):
    toWindow2_signal = pyqtSignal()
    toWindow4_signal = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__()
        uic.loadUi('./ui/startWindow2.ui', self)
        self.resize(1920, 1080)
        self.move(0, 0)
        self.groupBox.move(150, 134)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.eegImpTable.setRowCount(1)
        self.eegImpTable.setColumnCount(10)
        self.eegImpTable.setHorizontalHeaderLabels(["gnd", "ref", "afz", "af3", "af4",
                                                    "af7", "af8", "pz", "p3", "p4"])

        # 设置 eegImpTable 列宽为平均宽度
        self.set_table_column_widths()
        # 设置表格不可编辑
        self.eegImpTable.setEditTriggers(QTableWidget.NoEditTriggers)
        # 必要对象
        self.gazepointService = GazepointService()
        self.gazepointService.calibration_complete.connect(self.calibraResultFunction)

        self.websocketClient = WebSocketClient()
        self.websocketClient.data_received.connect(self.eegImpData)
        self.websocketClient.start()

        # 按钮事件绑定
        self.backBtn.clicked.connect(self.backWindowFunction)
        self.calibraeBtn.clicked.connect(self.calibraeFunction)
        self.nextPageBtn.clicked.connect(self.nextWindowFunction)
        self.calBtn.clicked.connect(self.calibraeEEGFunction)
        self.finishBtn.clicked.connect(self.finishEEGImpFunction)

        # self.setup_plots()
        # # WebSocket client
        # self.ws_client = WebSocketClient()
        # self.ws_client.start()

        # Start timer to update plots
        # self.timer = QTimer()
        # self.timer.timeout.connect(self.update_plots)
        # self.timer.start(1000 / 50)  # Update plots at 125Hz
    def finishEEGImpFunction(self):
        self.websocketClient.send_data("acquisition")
    def calibraeEEGFunction(self):
        self.websocketClient.send_data("calibration")
    def eegImpData(self, dataStr):
        data_values = self.parse_data(dataStr)
        if isinstance(data_values, list):
            # 更新表格的第一行
            for col, value in enumerate(data_values):
                int_value = int(float(value))  # 将浮点数转换为整数
                item = QTableWidgetItem(str(int_value))
                item.setFlags(item.flags() & ~Qt.ItemIsEditable)  # 设置单元格不可编辑
                item.setTextAlignment(Qt.AlignCenter)  # 设置文本居中对齐
                self.eegImpTable.setItem(0, col, item)

    def parse_data(self, data_string):
        # 使用ast.literal_eval安全地解析字符串数据为列表
        # 移除非 ASCII 字符
        if data_string.startswith('[') and data_string.endswith(']'):
            data_string = re.sub(r'[^\x00-\x7F]+', '', data_string)
            try:
                return ast.literal_eval(data_string)
            except (ValueError, SyntaxError) as e:
                print(f"Error parsing data: {e}")
                return None
    def set_table_column_widths(self):
        header = self.eegImpTable.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.Stretch)

    def calibraeFunction(self):
        self.gazepointService.start()
        self.calibraeResult.setText("校准结果:校准中")
        self.calibraeBtn.setEnabled(False)


    def calibraResultFunction(self,flag):
        # 如果已经校准完成且正确，则提示校准成功
        reslut = "校准成功" if flag else "校准失败"
        self.calibraeResult.setText("校准结果:"+ reslut)
        self.calibraeBtn.setEnabled(True)

    def backWindowFunction(self):
        self.toWindow2_signal.emit()

    def nextWindowFunction(self):
        self.toWindow4_signal.emit()



    # 脑电波形图数据更新
    # def update_plots(self):
    #     if self.ws_client.data_buffer:
    #         data = self.ws_client.data_buffer.pop(0)
    #         for i, plot in enumerate(self.plots):
    #             for c in self.curves[i]:
    #                 c.setPos(-(pg.ptime.time() - self.startTime), 0)
    #
    #             j = self.ptr % self.chunkSize
    #             if j == 0:
    #                 curve = plot.plot(pen='c')  # 设置线条颜色为天蓝色
    #                 self.curves[i].append(curve)
    #                 last = self.data[i][-1]
    #                 self.data[i] = np.empty((self.chunkSize + 1, 2))
    #                 self.data[i][0] = last
    #                 while len(self.curves[i]) > self.maxChunks:
    #                     c = self.curves[i].pop(0)
    #                     plot.removeItem(c)
    #             else:
    #                 curve = self.curves[i][-1]
    #
    #             self.data[i][j + 1, 0] = pg.ptime.time() - self.startTime
    #             self.data[i][j + 1, 1] = data[i]
    #             curve.setData(x=self.data[i][:j + 2, 0], y=self.data[i][:j + 2, 1])
    #
    #         self.ptr += 1
    #



    # 脑电波形图绘制
    # def setup_plots(self):
    #
    #     # Create a QGroupBox for plots
    #     group_box_layout = QVBoxLayout()
    #
    #     self.plots = []
    #     self.curves = []
    #     self.chunkSize = 100
    #     self.maxChunks = 10
    #     self.startTime = pg.ptime.time()
    #     self.ptr = 0
    #     self.data = [np.empty((self.chunkSize + 1, 2)) for _ in range(8)]
    #
    #     for i in range(8):
    #         plot = pg.PlotWidget()
    #         plot.setBackground('#f0f0f0')  # 设置背景色为白色
    #         plot.setXRange(-10, 0)
    #         group_box_layout.addWidget(plot)
    #         plot.setMouseEnabled(x=False, y=False)  # 禁止曲线图拖动
    #
    #         self.plots.append(plot)
    #         self.curves.append([])
    #         curve = plot.plot(pen='c')  # 设置线条颜色为天蓝色
    #         self.curves[i].append(curve)
    #
    #     self.naodian.setLayout(group_box_layout)


