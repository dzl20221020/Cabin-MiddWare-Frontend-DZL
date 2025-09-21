import sys
import json
import numpy as np
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
    update_plot_signal = pyqtSignal(list)

    def __init__(self, parent=None):
        super().__init__(parent)

    def process_message(self, message):
        try:
            # Try to parse JSON data
            json_data = json.loads(message)
            # Extract data for all channels
            data = json_data["data"]
            # Emit signal to update plot
            self.update_plot_signal.emit(data)
            # Print received message
            print("Received message:", message)
        except json.JSONDecodeError:
            # Print invalid message
            print("Invalid JSON message:", message)
        except KeyError:
            # Print missing key message
            print("Missing key in JSON message:", message)
        except Exception as e:
            # Print other exceptions
            print("Error:", e)

class PlotThread(QThread):
    update_plot_signal = pyqtSignal(list)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.data = [np.random.rand(250) for _ in range(8)]

    def set_data(self, data):
        self.data = data

    def run(self):
        while True:
            self.msleep(100)  # Update every 100 milliseconds
            self.update_plot_signal.emit(self.data)

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

        # Create subplots for each channel
        self.num_channels = 8
        self.fig, self.axes = plt.subplots(self.num_channels, 1, figsize=(8, 6), sharex=True)
        self.lines = [ax.plot([], [], lw=1, color='black')[0] for ax in self.axes]
        for ax in self.axes:
            ax.set_ylabel('Amplitude', fontsize=12)
            ax.set_ylim(-1, 1)
            ax.grid(True, linestyle='--', alpha=0.3)
            ax.spines['top'].set_visible(False)
            ax.spines['right'].set_visible(False)
            ax.tick_params(axis='both', which='both', labelsize=10)

        self.canvas = FigureCanvas(self.fig)
        layout.addWidget(self.canvas)

        # Create signal handler object
        self.signal_handler = SignalHandler()
        # Create plot thread object
        self.plot_thread = PlotThread()
        # Connect signal and slot
        self.signal_handler.update_plot_signal.connect(self.plot_thread.set_data)

        # Create and start WebSocket thread
        self.websocket_thread = WebSocketThread()
        self.websocket_thread.messageReceived.connect(self.signal_handler.process_message)
        self.websocket_thread.start()

        # Connect plot thread signal
        self.plot_thread.update_plot_signal.connect(self.update_plot)
        # Start plot thread
        self.plot_thread.start()

    def update_plot(self, data):
        # Update data for each channel
        for line, channel_data in zip(self.lines, data):
            line.set_ydata(channel_data)

        # Redraw canvas
        self.canvas.draw()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = BrainWaveWindow()
    window.show()
    sys.exit(app.exec_())
