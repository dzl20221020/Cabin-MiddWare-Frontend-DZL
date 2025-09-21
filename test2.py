import sys
import json
import random
from PyQt5.QtCore import QTimer, QObject, pyqtSignal, QThread
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt
import websocket

class WebSocketThread(QThread):
    messageReceived = pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent)

    def run(self):
        websocket.enableTrace(False)
        self.ws = websocket.WebSocketApp("ws://localhost:8888/websocket/display",
                                          on_message=self.on_message)
        self.ws.run_forever()

    def on_message(self, ws, message):
        # print(message)
        self.messageReceived.emit(message)

class SignalHandler(QObject):
    update_plot_signal = pyqtSignal(list)

    def __init__(self, parent=None):
        super().__init__(parent)

    def process_message(self, message):
        try:
            # Try to parse JSON data
            json_data = json.loads(message)
            # Extract data
            data = json_data["data"]
            # Emit signal to update plot
            self.update_plot_signal.emit(data)
            # 打印收到的消息
            # print("Received message:", message)
        except json.JSONDecodeError:
            # 打印无效的消息
            print("Invalid JSON message:", message)
        except KeyError:
            # 打印缺少必要字段的消息
            print("Missing key in JSON message:", message)
        except Exception as e:
            # 打印其他异常
            print("Error:", e)

class BrainWaveWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Set up main window
        self.setWindowTitle("Dynamic Brainwave Visualization")
        self.setGeometry(100, 100, 800, 600)

        # Set up central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        # Add matplotlib plot
        self.fig, self.axes = plt.subplots(nrows=8, ncols=1, figsize=(8, 10), sharex=True)
        self.lines = [ax.plot([], [], lw=2)[0] for ax in self.axes]
        self.x_data = [i for i in range(100)]
        self.y_data = [[0] * 100 for _ in range(8)]
        for ax in self.axes:
            ax.set_ylim(-1, 1)
        self.canvas = FigureCanvas(self.fig)
        layout.addWidget(self.canvas)

        # 创建信号处理器对象
        self.signal_handler = SignalHandler()
        # 连接信号槽
        self.signal_handler.update_plot_signal.connect(self.update_plot)

        # 创建并启动WebSocket线程
        self.websocket_thread = WebSocketThread()
        self.websocket_thread.messageReceived.connect(self.on_message)
        self.websocket_thread.start()

    def update_plot(self, data):
        # Update plot for each channel
        for i, ax in enumerate(self.axes):
            # Shift existing data to the left and append new data
            self.y_data[i] = self.y_data[i][1:] + [data[i]]

            # Update plot
            self.lines[i].set_data(self.x_data, self.y_data[i])

            # Adjust y-axis range
            min_amplitude = min(self.y_data[i])
            max_amplitude = max(self.y_data[i])
            buffer = 0.1 * (max_amplitude - min_amplitude)  # Add a buffer for better visualization
            ax.set_ylim(min_amplitude - buffer, max_amplitude + buffer)

        # Redraw canvas
        self.canvas.draw()

    def on_message(self, message):
        # 发送消息到主线程处理
        self.signal_handler.process_message(message)


if __name__ == "__main__":
    # Create PyQt5 application
    app = QApplication(sys.argv)
    # Create main window
    window = BrainWaveWindow()
    # Show main window
    window.show()
    # Start event loop
    sys.exit(app.exec_())
