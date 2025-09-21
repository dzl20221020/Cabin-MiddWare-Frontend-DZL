# -*- coding: utf-8 -*-

import threading

import websocket
from PyQt5.QtCore import QThread, pyqtSignal


class ExperimentWebSocketClient(QThread):
    data_received = pyqtSignal(str)

    def __init__(self):
        super(ExperimentWebSocketClient, self).__init__()
        self.lock = threading.Lock()
        self.url = "ws://127.0.0.1:8888/websocket/experimentStatusServer?username=touchscreen"
        self.ws = None

    def on_message(self, ws, message):
        print(message)
        # 返回试验状态到主进程
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