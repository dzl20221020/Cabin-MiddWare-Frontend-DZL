# import sys
# import random
# from PyQt5.QtCore import QTimer
# from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
# from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
# import matplotlib.pyplot as plt
#
# class BrainWaveWindow(QMainWindow):
#     def __init__(self):
#         super().__init__()
#
#         # Set up main window
#         self.setWindowTitle("Dynamic Brainwave Visualization")
#         self.setGeometry(100, 100, 800, 600)
#
#         # Set up central widget
#         central_widget = QWidget()
#         self.setCentralWidget(central_widget)
#         layout = QVBoxLayout(central_widget)
#
#         # Add matplotlib plot
#         self.fig, self.ax = plt.subplots()
#         self.x_data = [i for i in range(100)]
#         self.y_data = [0] * 100
#         self.line, = self.ax.plot(self.x_data, self.y_data, lw=2, color='lightblue')  # Set line color
#         self.ax.set_ylabel('Amplitude', fontsize=12)  # Set y-axis label
#         self.ax.set_ylim(-1, 1)
#         self.ax.grid(True, linestyle='--', alpha=0.6)  # Add grid lines
#         self.ax.spines['top'].set_visible(False)  # Hide top and right spines
#         self.ax.spines['right'].set_visible(False)
#         self.ax.tick_params(axis='both', which='both', labelsize=10)  # Set tick label size
#         self.canvas = FigureCanvas(self.fig)
#         layout.addWidget(self.canvas)
#
#         # Set up QTimer to update plot
#         self.timer = QTimer()
#         self.timer.timeout.connect(self.update_plot)
#         self.timer.start(100)  # Update plot every 100 milliseconds
#
#     def update_plot(self):
#         # Generate random data
#         new_data = random.uniform(-1, 1)
#
#         # Shift existing data to the left and append new data
#         self.y_data = self.y_data[1:] + [new_data]
#
#         # Update plot
#         self.line.set_ydata(self.y_data)
#
#         # Redraw canvas
#         self.canvas.draw()
#
# if __name__ == "__main__":
#     # Create PyQt5 application
#     app = QApplication(sys.argv)
#     # Create main window
#     window = BrainWaveWindow()
#     # Show main window
#     window.show()
#     # Start event loop
#     sys.exit(app.exec_())


import sys
import json
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
        print(message)
        self.messageReceived.emit(message)

class SignalHandler(QObject):
    update_plot_signal = pyqtSignal(float)

    def __init__(self, parent=None):
        super().__init__(parent)

    def process_message(self, message):
        try:
            # Try to parse JSON data
            json_data = json.loads(message)
            # Extract amplitude data
            amplitude = json_data["data"][0]
            # Emit signal to update plot
            self.update_plot_signal.emit(amplitude)
            # 打印收到的消息
            print("Received message:", message)
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
        self.fig, self.ax = plt.subplots()
        self.x_data = [i for i in range(100)]
        self.y_data = [0] * 100
        self.line, = self.ax.plot(self.x_data, self.y_data, lw=2)
        self.ax.set_ylabel('Amplitude')
        self.ax.set_ylim(-1, 1)
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

    def update_plot(self):
        pass  # 将此方法留空，因为它将由信号触发更新

    def on_message(self, message):
        # 发送消息到主线程处理
        self.signal_handler.process_message(message)

    def update_plot(self, amplitude):
        # Shift existing data to the left and append new data
        self.y_data = self.y_data[1:] + [amplitude]

        # Update plot
        self.line.set_ydata(self.y_data)

        # Adjust y-axis range
        min_amplitude = min(self.y_data)
        max_amplitude = max(self.y_data)
        buffer = 0.1 * (max_amplitude - min_amplitude)  # Add a buffer for better visualization
        self.ax.set_ylim(min_amplitude - buffer, max_amplitude + buffer)

        # Adjust x-axis range
        self.ax.set_xlim(0, len(self.y_data))

        # Redraw canvas
        self.canvas.draw()


if __name__ == "__main__":
    # Create PyQt5 application
    app = QApplication(sys.argv)
    # Create main window
    window = BrainWaveWindow()
    # Show main window
    window.show()
    # Start event loop
    sys.exit(app.exec_())

