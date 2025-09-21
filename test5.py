import sys
import json
import numpy as np
import pyqtgraph as pg
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
from websocket import create_connection

class EEGDisplay(QMainWindow):
    def __init__(self):
        super(EEGDisplay, self).__init__()

        self.initUI()
        self.connect_to_websocket()

    def initUI(self):
        centralWidget = QWidget()
        self.setCentralWidget(centralWidget)

        layout = QVBoxLayout()
        centralWidget.setLayout(layout)

        self.plot_widgets = []
        self.curves = []

        background_color = '#f0f0f0'

        for i in range(8):
            plot_widget = pg.PlotWidget()
            plot_widget.setBackground(background_color)
            plot_widget.showGrid(x=True, y=True, alpha=0.5)
            layout.addWidget(plot_widget)
            self.plot_widgets.append(plot_widget)
            curve = plot_widget.plot(pen=(i, 8), width=2)
            self.curves.append(curve)

        self.setGeometry(100, 100, 1200, 800)
        self.setWindowTitle('EEG Display')
        self.show()

    def connect_to_websocket(self):
        self.ws = create_connection("ws://localhost:8765")

    def update_plot(self, eeg_data):
        x_data = np.arange(len(eeg_data[0]))  # 使用数组的索引作为横坐标
        for i in range(8):
            self.curves[i].setData(x_data, eeg_data[i])

            # 将横坐标范围设置为当前数据索引的最大值
            self.plot_widgets[i].setXRange(max(0, x_data[-1] - 100), x_data[-1])

    def auto_range(self):
        pass  # 不再调整横坐标范围

def simulate_websocket_data():
    while True:
        data = {"channels":"8","data":np.random.rand(8, 100).tolist(),"deviceId":"101402-0002_Impedance","protocolV":"1.0","timeStamp":"0.0","type":"101402-0002_Impedance"}
        yield json.dumps(data)

def parse_websocket_data(data):
    try:
        parsed_data = json.loads(data)
        eeg_data = np.array(parsed_data["data"])
        return eeg_data.reshape((int(parsed_data["channels"]), -1))
    except json.JSONDecodeError:
        print("Error parsing JSON data")
        return None

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = EEGDisplay()

    websocket_data = simulate_websocket_data()

    def update():
        raw_data = next(websocket_data)
        eeg_data = parse_websocket_data(raw_data)
        if eeg_data is not None:
            ex.update_plot(eeg_data)

    timer = pg.QtCore.QTimer()
    timer.timeout.connect(update)
    timer.start(1000)  # 控制数据更新频率，这里设置为1秒

    sys.exit(app.exec())
