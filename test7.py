import pyqtgraph as pg
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import pyqtSignal, QObject
import numpy as np
import websocket
import json
import threading

class EEGDataStreaming(QObject):
    update_signal = pyqtSignal(np.ndarray)

    def __init__(self, websocket_server_address):
        super().__init__()
        self.websocket_server_address = websocket_server_address
        self.buffer_size = 300  # 缓冲区大小
        self.data_buffer = np.zeros((8, self.buffer_size))  # 初始化数据缓冲区
        self.buffer_index = 0  # 缓冲区索引

        # 创建一个应用程序对象
        self.app = QApplication.instance() or QApplication([])

        # 创建一个窗口
        self.win = pg.GraphicsLayoutWidget(show=True)
        self.win.setWindowTitle('EEG Data Streaming')
        self.win.resize(800, 600)

        # 设置窗口的背景为浅蓝色
        self.win.setBackground('w')

        # 添加八个绘图
        self.plots = []
        for i in range(8):
            plot = self.win.addPlot(row=i, col=0)
            plot.setLabel('left', f'Channel {i+1}', units='uV')
            plot.setMouseEnabled(x=False, y=False)  # 禁用拖动功能
            # 获取视图框对象并设置背景颜色
            view = plot.getViewBox()
            view.setBackgroundColor('w')  # 设置图的背景为浅蓝色
            self.plots.append(plot)

        # 连接更新信号到更新函数
        self.update_signal.connect(self.update)

    # 更新函数
    def update(self, data):
        for i, plot in enumerate(self.plots):
            plot.clear()
            plot.plot(data[i], pen=pg.mkPen(color='#87CEEB'))  # 设置线条颜色为浅蓝色

    # WebSocket 接收数据的回调函数
    def on_message(self, ws, message):
        # 解析收到的数据
        data_dict = json.loads(message)
        eeg_data = data_dict['data']
        new_data = np.array(eeg_data)

        # 将新数据插入到缓冲区的末尾
        self.data_buffer = np.roll(self.data_buffer, -1, axis=1)
        self.data_buffer[:, -1] = new_data

        # 发送更新信号
        self.update_signal.emit(self.data_buffer)

    # WebSocket 连接函数
    def ws_thread(self):
        ws = websocket.WebSocketApp(self.websocket_server_address, on_message=self.on_message)
        ws.run_forever()

    # 启动数据流
    def start(self):
        # 创建并启动后台线程
        thread = threading.Thread(target=self.ws_thread)
        thread.daemon = True
        thread.start()

        # 启动 Qt 事件循环
        self.app.exec_()

# WebSocket 服务器地址和端口
websocket_server_address = "ws://localhost:8765"

# 创建数据流对象并启动数据流
eeg_data_streaming = EEGDataStreaming(websocket_server_address)
eeg_data_streaming.start()
